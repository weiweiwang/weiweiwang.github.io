title: Compress js and css with YUI Compressor Maven Mojo
slug: compress-js-css-with-yui-compressor-maven-pojo
category: misc
tags: js,css,yui,compressor,maven

# 配置

    <pluginRepositories>
        <pluginRepository>
            <name>oss.sonatype.org</name>
            <id>oss.sonatype.org</id>
            <url>http://oss.sonatype.org/content/groups/public</url>
        </pluginRepository>
    </pluginRepositories>
    <plugin>
                <groupId>net.alchim31.maven</groupId>
                <artifactId>yuicompressor-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>compress</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <nosuffix>true</nosuffix>
                    <sourceDirectory>${project.basedir}/web</sourceDirectory>
                    <outputDirectory>${project.build.directory}/web</outputDirectory>
                </configuration>
            </plugin>

# 注意事项
这个plugin拷贝js/css文件到制定的目录中，并且会保留原有的目录结构，比如web目录下有js,css这两个文件夹，那么输出的目录target/web中也会有同样的目录结构。但是如果你的web目录下还有其他文件，比如html等，这个plugin不会帮你拷贝到target/web目录下的，这时候需要结合使用maven-resources插件，举例:

        <resources>
            <resource>
                <directory>${project.basedir}/web/public/images</directory>
                <targetPath>${project.build.directory}/web/public/images</targetPath>
            </resource>
            <resource>
                <directory>${project.basedir}/web/public/static</directory>
                <targetPath>${project.build.directory}/web/public/static</targetPath>
            </resource>
        </resources>


# 参考

1. [YUI Compressor Maven Mojo](http://alchim.sourceforge.net/yuicompressor-maven-plugin/compress-mojo.html)

