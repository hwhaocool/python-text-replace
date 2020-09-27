# python-text-replace
filter then find and replace text config by json wirte by python  

通过配置文件，先找到文件列表，然后对列表依次应用配置里的 替换规则列表

[中文介绍](https://github.com/hwhaocool/python-text-replace/wiki/%E4%B8%AD%E6%96%87%E4%BB%8B%E7%BB%8D)

## example

here we have a file  
```
package com.xxx.be.doc.model;

public class Hello {
    private String name;

    private Integer age;
}
```

I want find the file and then replace the package statement to  
`package com.xxx.be.doc;`  
(this tool will only replace the text, will not remove the file to exactly path)

First, config the filter rule to find the files  
(the rule will apply for its contents, not file name)  
```
filter:
  - name: filterMyDoc
    contains: be.doc.model
```

Second, config the replace rule 
```
replace:
  - name: replacePackage
    filterRuleName: filterMyDoc
    actions:
      - matchStr: package com.xxx.be.doc.model
        replace: package com.xxx.be.doc
```

Then, run script and input the dst path

```
D:\>python app.py
config.json load completed
please input a number to select a function:
1  --  filter and print file name
2  --  filter then find and replace

2

**********  filter , find , replace   ***
1   replacePackage
2   replaceImport
3   replaceDocInService
4   replacePicInfo
please input a number to select a config:

1

please input path: D:\006-project\yellowtail\python-text-replace\test

contains -- xxx
dstPath have 2 files
match 1 files
not match 1 files
replace 0

```