title: Java程序CPU使用分析
slug: java-cpu-usage-analysis
category: programming
tags: java,cpu,usage,top,jstack,kill

# 用top找出cpu消耗过高的java进程



	top - 11:49:39 up 1 day,  1:53,  8 users,  load average: 0.24, 0.13, 0.22
	Tasks: 210 total,   2 running, 203 sleeping,   0 stopped,   5 zombie
	Cpu(s):  7.8%us,  3.7%sy,  0.1%ni, 87.2%id,  1.0%wa,  0.0%hi,  0.2%si,  0.0%st
	Mem:   3343444k total,  2968552k used,   374892k free,    84140k buffers
	Swap:  1951860k total,   631640k used,  1320220k free,   420808k cached
	  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
	16423 wangweiw  20   0  677m 205m 8900 S  101  6.3   0:14.16 java
	 6783 wangweiw  20   0 1750m 1.1g  33m S    6 35.8 149:45.22 java
	 1246 root      20   0  234m  57m  12m S    2  1.8  46:16.49 Xorg

比如我们分16423析这个java进程。
# 查看cpu消耗过高的线程。
	
	top -H -p 16423

	  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
	16457 wangweiw  20   0  677m 209m 8900 R  100  6.4   2:30.00 java
	16423 wangweiw  20   0  677m 209m 8900 S    0  6.4   0:00.00 java
	16424 wangweiw  20   0  677m 209m 8900 S    0  6.4   0:01.24 java

然后我们再分析16457这个线程

# 用jstack分析线程栈
	jstack $pid|grep -A N $nid
此处的pid就是16423, nid就是16457，由于jstack输出中的thread id是16进制的，所以要把16457转换成16进制:4049。grep命令中的-A表示显示后面若干行，比如这里显示了grep到的行的后面10行，这个可以根据输出来调整。

	jstack 16423|grep -A 10 4049
	"qtp16147692-26" prio=10 tid=0x8e7e5c00 nid=0x4049 runnable [0x8e133000]
	   java.lang.Thread.State: RUNNABLE
		at org.restlet.engine.http.header.HeaderReader.addValues(HeaderReader.java:254)
		at org.restlet.engine.http.ServerCall.getRequestEntity(ServerCall.java:215)
		at org.restlet.engine.http.HttpRequest.getEntity(HttpRequest.java:488)
		at org.restlet.engine.application.Decoder.beforeHandle(Decoder.java:123)
		at org.restlet.routing.Filter.handle(Filter.java:204)
		at org.restlet.routing.Filter.doHandle(Filter.java:159)
		at org.restlet.engine.application.StatusFilter.doHandle(StatusFilter.java:155)
		at org.restlet.routing.Filter.handle(Filter.java:206)
		at org.restlet.routing.Filter.doHandle(Filter.java:159)

# 跟踪代码定位问题
此处这个程序是使用了Restlet框架做的一个web服务，addValues这个方法体如下：

	  public void addValues(Collection<V> values) {
	        try {
	            // Skip leading spaces
	            skipSpaces();
	
	            do {
	                // Read the first value
	                V nextValue = readValue();
	                if (canAdd(nextValue, values)) {
	                    // Add the value to the list
	                    values.add(nextValue);
	                }
	
	                // Attempt to skip the value separator
	                skipValueSeparator();
	            } while (peek() != -1);
	        } catch (IOException ioe) {
	            Context.getCurrentLogger().log(Level.INFO,
	                    "Unable to read a header", ioe);
	        }
	    }

看到这里有个while循环，再分析下skipSpaces,readValue,peek几个函数后就很容易构造一个死循环的例子：
	
	EncodingReader encodingReader = new EncodingReader("修改gzip");
	encodingReader.addValues(new ArrayList());

这个bug虽然命中概率很低，但是一旦命中，程序瞬间就崩溃了，这个问题在我们一个服务里遇到，只要用户的某次请求的header出现非法字符，一个线程就被占用并且是100% cpu占用，虽然这样的请求可能一天只有一个，但几天之后服务器cpu load就高的不行，只能重启程序解决。当然这样肯定不是长远的解决方案，更好的方案是在前端nginx上override出问题的header，来避免这样的请求进入到restlet代码层，目前看来进入restlet代码层，我们的程序就无能为力了。比如出问题的header是Content-Encoding,那么nginx的location可以配置如下:

	location / {
	          proxy_pass http://xxx_upstream;
	          proxy_set_header Host $host;
	          proxy_set_header Content-Encoding gzip;
	          proxy_set_header        X-Real-IP $remote_addr;
	          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	          proxy_connect_timeout 6;
	          proxy_read_timeout 60;
	          proxy_send_timeout 60;
	        }
当然也可以修改restlet源代码解决，不过这样后续升级restlet的时候会麻烦一些。
