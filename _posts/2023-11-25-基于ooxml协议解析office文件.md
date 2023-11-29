---
layout:       post
title:        "基于ooxml协议解析office文件"
author:       "mjTree"
header-style: text
catalog:      true
tags:
    - document-parse
    - ooxml
---

><small>更新于：2023-11-28 23:37</small>  


### 一、OOXML协议

引用 [**官方网站**](http://officeopenxml.com/) 的一句话：

> Office Open XML，也称为 OpenXML 或 OOXML，是一种基于 XML 的办公文档格式，包括文字处理文档、电子表格、演示文稿以及图表、图表、形状和其他图形材料。

该规范由`Microsoft`开发，并于 2006 年被`ECMA International`采用为`ECMA-376`。尽管`Microsoft`继续支持较旧的二进制格式（.doc、xls 和 .ppt），但`OOXML`现在是所有 Microsoft Office 文档（.docx、.xlsx 和 .pptx）的默认格式。协议定义了`Markup specifications`（标记规范）以及`A file packaging specification`（文件打包规范）。  


### 二、OOXML的标记规范
它不仅包括主要的三种办公文档类型中的不同规范，分别是：用于文字处理文档的`WordprocessingML`、用于电子表格文档的`SpreadsheetML`以及用于演示文稿文档的`PresentationML`。它还包括一些支持标记语言，核心的是用于绘图、形状和图表的 DrawingML。该规范包括书面形式的 XML 模式和约束。任何符合标准的文档都必须符合 XML 模式，并且采用 UTF-8 或 UTF-16 编码。该规范确实包含一些可扩展性机制，允许自定义 XML 与 OOXML 标记一起存储。  


### 三、OOXML的文件打包规范
协议定义了开放封装约定 (OPC)，`OPC` 是一种容器文件技术，利用通用 ZIP 格式将文件组合到通用包中。因此 OOXML 协议组成的文件，是一个包含各种 XML 文件（部分）并组织到单个包中的 ZIP 存档。将数据分解或分块可以更轻松、更快速地访问数据，并减少数据损坏的机会。这些部分可以包含任何类型的数据；为了在不依赖文件扩展名的情况下跟踪每个部分的数据类型，每个部分的类型在包内名为 [Content_Types].xml 的文件中指定。部件与包的关系以及任何部件可能具有的关系从部件中抽象出来并单独存储在关系文件中，一个用于整个包，一个用于每个具有关系的包。通过这种方式，引用仅存储一次，因此可以在必要时轻松更改。  

接下来通过下图的展示以及相关描述，来给大家展示 OOXML 是如何组建一个文件的。  

![format_display](/img/article-img/2023/1125_1.png)

![format_display](/img/article-img/2023/1125_2.png)

首先将一个 .docx 文件的后缀修改成一个 .zip 格式，借用解压软件进行解压变能够看到内部的文件存储结构


### 四、解析由ooxml协议构成的文件




### 五、小结




