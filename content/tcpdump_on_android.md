title: Android上用Tcpdump抓包
slug: android-tcpdump
category: android
tags: tcpdump,android
date: 2012-08-25

#下载
下载tcpdump， 还有个地址是http://www.eecs.umich.edu/~timuralp/tcpdump-arm，下载重命名为tcpdump

# 使用
详细使用请参考http://www.tcpdump.org/里面的文档

机器是需要root过才能使用tcpdump的。

	adb push c:/wherever_you_put/tcpdump /data/local/tcpdump
	adb shell chmod 6755 /data/local/tcpdump

抓包很简单(需要root权限）
	
	adb shell
	su（这个是换成root用户）
	/data/local/tcpdump -p -vv -s 0 -w /sdcard/capture.pcap

接着就会看到：
	
	tcpdump: listening on wlan0, link-type EN10MB (Ethernet), capture size 65535 bytes
	Got 0

CTRL—C停止抓包，然后两次exit，再然后：
	
	adb pull /sdcard/capture.pcap

最后用wireshark在pc机上就可以分析了。

下载wireshark查看数据包，地址是http://www.wireshark.org/download.html，打开这个数据包，就可以查看了。


