;
(function($, window){

	function Jqcloud(word_array, config, selector) {
		// 默认配置
		var defaults = {
			afterCloudRender: null,
			autoResize: true,
			width: 100,
			height: 100,
			center: { x: 0.5, y: 0.5 },
			steps: 10,
			shape: 'elliptic',
			classPattern: 'w{n}',
			removeOverflowing: true,
			encodeURI: true,
			colors: [],
			fontSize: null,
			delay: null,
			template: null
		};
		// 选择器句柄
		this.$selector = selector;
		this.word_array = word_array || [];
		// 设置/获得尺寸
		var self = this;
		var $selector = self.$selector;
		var options = typeof config === 'object' ? config : {};
		if(!options.width) {
			options.width = $selector.width();
		}
		if(!options.height) {
			options.height = $selector.height();
		}
		// 继承后配置
		this.config = $.extend(defaults, config, options);
		// 初始化
		this.init();
	};

	Jqcloud.prototype.init = function() {
		var self = this;
		var $selector = self.$selector;
		self.setVars();
		self.appendSizes();
		self.clearTimeouts();
		self.calculateAll();
		self.createTimeout($.proxy(self.drawWordCloud, self), 10);
		self.response();
	};

	// 设置全局变量
	Jqcloud.prototype.setVars = function() {
		var self = this;
		var $selector = self.$selector;
		self.$element = $($selector);
		self.placed_words = [];
		self.timeouts = {};
		self.namespace = null;
		self.angle = null;
		self.aspect_ratio = null;
		self.max_weight = null;
		self.min_weight = null;
		self.sizes = [];
		self.step = null;
		self.colorGenerator = null;
	};

	// 添加样式
	Jqcloud.prototype.appendSizes = function() {
		var self = this;
		var config = self.config;
		var $selector = self.$selector;
		var cl;
		var i;
		self.$element.addClass('jqcloud');
		if (typeof config.colors == 'function') {
			self.colorGenerator = config.colors;
		} else if ($.isArray(config.colors)) {
			cl = config.colors.length;
			if (cl > 0) {
				if(cl < config.steps) {
					for(i = cl; i < config.steps; i++) {
						config.colors[i] = config.colors[cl-1];
					}
				}
			}
			self.colorGenerator = function(weight) {
				return config.colors[config.steps - weight];
			}
		}
	};

	// 清除时钟
	Jqcloud.prototype.clearTimeouts = function() {
		var self = this;
		$.each(self.timeouts, function(key) {
			clearTimeout(key);
		});
		self.timeouts = {};
	};

	// 计算
	Jqcloud.prototype.calculateAll = function() {
		var self = this;
		var config = self.config;
		var $selector = self.$selector;
		self.step = (config.shape === 'retangular') ? 18.0 : 2.0;
		self.aspect_ratio = config.width / config.height;
		// 命名空间中的字标识，以避免多个云之间的冲突
		self.namespace = ($selector.attr('id') || Math.floor((Math.random()*1000000)).toString(36)) + '_word_';
	};

	// 创造时钟
	Jqcloud.prototype.createTimeout = function(callback, time) {
		var self = this;
		var timeout = setTimeout($.proxy(function(){
			delete self.timeouts[timeout];
			callback();
		}, this), time);
		self.timeouts = {};
	};

	// 两两重叠检测
	Jqcloud.prototype.overlapping = function(a, b) {
		if (Math.abs(2.0 * a.left + a.width - 2.0 * b.left - b.width) < a.width + b.width) {
			if(Math.abs(2.0 * a.top + a.height - 2.0 * b.top - b.height) < a.height + b.height) {
				return true;
			}
		}
		return false;
	};

	// 如果一个元素与其他元素重叠，则辅助函数测试
	Jqcloud.prototype.hitTest = function(elem) {
		var self = this;
		// 检查元素的重叠一个一个，停止和返回的错误，尽快一个重叠被发现
		for(var i = 0, l = self.placed_words.length; i < l; i++) {
			if(self.overlapping(elem, self.placed_words[i])) {
				return true;
			}
		}
		return false;
	};

	// 初始化整个云的绘制
	Jqcloud.prototype.drawWordCloud = function() {
		var i, l;
		var self = this;
		var config = self.config;
		var $selector = self.$selector;
		$selector.children('[id^="' + self.namespace + '"]').remove();
		if (self.word_array.length === 0) {
			return;
		}
		for (i = 0,l = self.word_array.length; i < l; i++) {
			self.word_array[i].weight = parseFloat(self.word_array[i].weight, 10);
		}
		self.word_array.sort(function(a, b) {
			return b.weight - a.weight;
		});
		self.max_weight = self.word_array[0].weight;
		self.min_weight = self.word_array[self.word_array.length - 1].weight;
		self.colors = [];
		if(self.colorGenerator) {
			for(i = 0; i < config.steps; i++) {
				self.colors.push(self.colorGenerator(i + 1));
			}
		}
		if (config.delay > 0) {
			self.drawOneWordDelayed();
		} else {
			for (i = 0,l = self.word_array.length; i < l; i++) {
				self.drawOneWord(i, self.word_array[i]);
			}
			if (typeof config.afterCloudRender === 'function') {
				config.afterCloudRender.call(self.$element);
			}
		}
	};

	// 函数来画一个词，通过移动它在螺旋，直到它找到一个合适的空位置
	Jqcloud.prototype.drawOneWord = function(index, word) {
		var self = this;
		var config = self.config;
		var $selector = self.$selector;
		var word_id = self.namespace + index;
		var word_selector = '#' + word_id;
		var angle = self.angle;
		var radius = 0.0;
		var steps_in_direction = 0.0;
		var quarter_turns = 0.0;
		var weight = Math.floor(self.steps / 2);
		var word_span;
		var word_size;
		var word_style;
		// 创建Word属性对象
		word.attr = $.extend({}, word.html, { id: word_id });
		// 线性映射原权重到一个离散尺度从1到10
		// 只有权重是不同的
		if(self.max_weight != self.min_weight) {
			weight = Math.round((word.weight - self.min_weight) * 1.0 * (config.steps - 1) / (self.max_weight - self.min_weight)) + 1;
		}
		word_span = $('<span>').attr(word.attr);
		// 应用类
		if(config.classPattern) {
			word_span.addClass(config.classPattern.replace('{n}', weight));
		}
		// 应用颜色
		if(self.colors.length) {
			word_span.css('color', self.colors[weight - 1]);
		}
		// 从字属性应用颜色
		if(word.color) {
			wrod_span.css('color', word.color);
		}
		// 如果提供使用模板函数
		if(config.template) {
			word_span.html(config.template(word));
		} else if (word.link) {
			// 附加链接如果word.link属性设置
			// 如果链接是一个字符串，然后使用它作为链接的href
			if(typeof word.link === 'string') {
				word.link = { href: word.link };
			}
			if(config.encodeURI) {
				word.link.href = encodeURI(word.link.href).replace(/'/g,'%27');
			}
			word_span.append($('<a>').attr(word.link).text(word.text));
		} else {
			word_span.text(word.text);
		}

		// 对每个单词绑定事件
        if (word.handlers) {
            word_span.on(word.handlers);
        }

		$selector.append(word_span);
		word_size = {
			width: word_span.outerWidth(),
			height: word_span.outerHeight()
		};
		word_size.left = config.center.x * config.width - word_size.width / 2.0;
		word_size.top = config.center.y * config.height - word_size.height / 2.0;
		// 保存对样式属性的引用，以更好的性能
		word_style = word_span[0].style;
		word_style.position = 'absolute';
		word_style.left = word_size.left + 'px';
		word_style.top = word_size.top + 'px';
		while(self.hitTest(word_size)) {
			// 选项的形状是“矩形”，所以把这个词在一个矩形的螺旋
			if (config.shape === 'rectangular') {
				steps_in_direction++;
				if(steps_in_direction * self.step > (1 + Math.floor(quarter_turns / 2.0)) * self.step * ((quarter_turns % 4 % 2) === 0 ? 1 : self.aspect_ratio)) {
					steps_in_direction = 0.0;
					quarter_turns++;
				}
				switch(quarter_turns % 4) {
					case 1:
						word_size.left += self.step * self.aspect_ratio + Math.random() * 2.0;
						break;
					case 2:
						word_size.top -= self.step + Math.random() * 2.0;
						break;
					case 3:
						word_size.left -= self.step * self.aspect_ratio + Math.random() * 2.0;
						break;
					case 0:
						word_size.top += self.step + Math.random() * 2.0;
						break;
				}
			}
			// 默认设置：椭圆螺旋形 
			else {
				radius += self.step;
				angle += (index % 2 === 0 ? 1 : -1) * self.step;
				word_size.left = config.center.x * config.width - (word_size.width / 2.0) + (radius * Math.cos(angle)) * self.aspect_ratio;
				word_size.top = config.center.y * config.height + radius * Math.sin(angle) - (word_size.height / 2.0);
			}
			word_style.left = word_size.left + 'px';
			word_style.top = word_size.top + 'px';
		}
		// 不要渲染字，如果它的一部分将在容器外
		if(config.removeOverflowing && (word_size.left < 0 || word_size.top < 0 || (word_size.left + word_size.width) > config.width || (word_size.top + word_size.height) > config.height)) {
			word_span.remove();
			return;
		}
		// 保存位置为进一步的使用
		self.placed_words.push(word_size);
 	};

 	// Draw one word then recall the function after a delay
    Jqcloud.prototype.drawOneWordDelayed = function(index) {
    	var self = this;
    	var config = self.config;

        index = index || 0;

        // if not visible then do not attempt to draw
        if (!this.$element.is(':visible')) {
            this.createTimeout($.proxy(function() {
                this.drawOneWordDelayed(index);
            }, this), 10);

            return;
        }

        if (index < this.word_array.length) {
            this.drawOneWord(index, this.word_array[index]);

            this.createTimeout($.proxy(function() {
                this.drawOneWordDelayed(index + 1);
            }, this), config.delay);
        }
        else {
            if (typeof config.afterCloudRender == 'function') {
                config.afterCloudRender.call(this.$element);
            }
        }
    },

 	// 更新单词列表
 	Jqcloud.prototype.update = function(word_array) {
 		var self = this;
 		self.word_array = word_array;
 		self.placed_words = [];
 		self.clearTimeouts();
 		self.drawWordCloud();
 	};

 	Jqcloud.prototype.resize = function() {
 		var self = this;
 		var config = self.config;
 		var $selector = self.$selector;
 		var new_size = {
 			width: $selector.width(),
 			height: $selector.height()
 		};
 		if (new_size.width != config || new_size.height != config.height) {
 			config.width = new_size.width;
 			config.height = new_size.height;
 			self.aspect_ratio = config.width / config.height;
 			self.update(self.word_array);
 		}
 	};

 	// 调节窗口
 	Jqcloud.prototype.response = function() {
 		var self = this;
 		var config = self.config;
 		/*
	   	* Apply throttling to a callback
	   	* @param callback {function}
	   	* @param delay {int} milliseconds
	   	* @param context {object|null}
	   	* @return {function}
	   	*/
 		self.throttle = function(callback, delay, context) {
 			var state = {
 				pid: null,
 				last: 0
 			};
 			return function() {
 				var elapsed = new Date().getTime() - state.last;
 				var args = arguments;
 				var that = this;
 				function exec() {
 					state.last = new Date().getTime();
 					return callback.apply(context || that, Array.prototype.slice.call(args));
 				}
 				if(elapsed > delay) {
 					return exec();
 				} else {
 					clearTimeout(state.pid);
 					state.pid = setTimeout(exec, delay - elapsed);
 				}
 			}
 		};
 		if(config.autoResize) {
 			$(window).on('resize',self.throttle(self.resize, 50, self));
 		}
 	};

	$.fn.Jqcloud = function(word_array, config) {
		var args = arguments;

		return this.each(function() {
			var $this = $(this),
				data = $this.data('Jqcloud');

			if(!data) {
				var configs = typeof config === 'object' ? config : {};
				$this.data('Jqcloud', (data = new Jqcloud(word_array, config, $this)));
			}
			else if (typeof word_array === 'string') {
				data[word_array].apply(data, Array.prototype.slice.call(args, 1));
			}
		});
	};

})(jQuery, window);