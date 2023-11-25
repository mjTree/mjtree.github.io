---
layout:       post
title:        "基于ooxml协议解析office文件"
author:       "mjTree"
header-style: text
catalog:      true
tags:
    - 文档结构化
    - OOXML
---

><small>更新于：2023-11-25 18:31</small>  


### 一、OOXML协议
引用 [**官方网站**](http://officeopenxml.com/) 的一句话：
>Office Open XML，也称为 OpenXML 或 OOXML，是一种基于 XML 的办公文档格式，包括文字处理文档、电子表格、演示文稿以及图表、图表、形状和其他图形材料。该规范由 Microsoft 开发，并于 2006 年被 ECMA International 采用为 ECMA-376。尽管 Microsoft 继续支持较旧的二进制格式（.doc、xls 和 .ppt），但 OOXML 现在是所有 Microsoft Office 文档（.docx、.xlsx 和 .pptx）的默认格式。


### 二、OOXML协议如何构建文件

除了标记语言规范之外，ECMA-376 第 2 部分还指定了开放封装约定 (OPC)。OPC 是一种容器文件技术，利用通用 ZIP 格式将文件组合到通用包中。因此，OOXML 文件是包含各种 XML 文件（部分）并组织到单个包中的 ZIP 存档。将数据分解或分块可以更轻松、更快速地访问数据，并减少数据损坏的机会。这些部分可以包含任何类型的数据；为了在不依赖文件扩展名的情况下跟踪每个部分的数据类型，每个部分的类型在包内名为 [Content_Types].xml 的文件中指定。部件与包的关系以及任何部件可能具有的关系从部件中抽象出来并单独存储在关系文件中——一个用于整个包，一个用于每个具有关系的包。通过这种方式，引用仅存储一次，因此可以在必要时轻松更改。


### 三、解析由ooxml协议构成的文件




### 四、小结




