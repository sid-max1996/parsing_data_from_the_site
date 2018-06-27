import urllib.request
import re

def CreateResFile():
    outfile = open('output.sql', 'w', encoding='utf-8')

    file1 = open('mainCategory.sql', 'r', encoding='utf-8')
    file2 = open('childrenCategory.sql', 'r', encoding='utf-8')
    file3 = open('items.sql', 'r', encoding='utf-8')
    file4 = open('linkItemsCat.sql', 'r', encoding='utf-8')

    outfile.write( file1.read() )
    outfile.write( file2.read() )
    outfile.write( file3.read() )
    outfile.write( file4.read() )

def SaveImg(url, imgPath):
    img = urllib.request.urlopen(url).read()
    out = open(imgPath, "wb")
    out.write(img)
    out.close()

def GetTitleAndDesc(driver, isPrint=False):
    title = driver.title
    if isPrint:
        print('title:' + title)
    description = ''
    try:
        headHtml = driver.find_element_by_tag_name("head")
        metaTags = headHtml.find_element_by_css_selector("meta[name='description']")
        description = metaTags.get_attribute('content')
        if isPrint:
            print('description:' + description)
    except Exception as e: 
        print(format(e))
    return title, description

def GetTableTitles(tr):
    tdArr = tr.find_elements_by_tag_name("th")
    titleArr = []
    for tdInd in range(len(tdArr)):
        text = tdArr[tdInd].get_attribute('innerHTML')
        text = text.strip()
        titleArr.append(text)
    return titleArr;

class CategoryParams:
    def __init__(self, id, appId, name, alias, content, imgPath, title, description, parent):
        self.id = id
        self.appId = appId
        self.name = name
        self.alias = alias
        self.content = content
        self.imgPath = imgPath
        self.title = title
        self.description = description
        self.parent = parent

aliasCount = 0
def GetCategoryTemplate(prefix, params):
    global aliasCount
    template = "INSERT INTO `{pref}_zoo_category` (`id`, `application_id`, `name`, `alias`, `description`, `parent`, `ordering`, `published`, `params`) VALUES".format(pref=prefix)
    template += "({id}, {appId}, '{name}', '{alias}', '{content}', {parent}, 1, 1, ".format(id=params.id, appId=params.appId, name=params.name, alias=params.alias+str(aliasCount), content=params.content, parent=params.parent)
    template += "'{\n	\"content.category_title\": \""+params.title+"\",\n	\"content.category_subtitle\": \"\",\n	\"content.category_teaser_text\": \"\",\n	"
    template += "\"content.category_image\": \"{imgPath}\",\n	\"content.category_image_width\": \"\",\n	\"content.category_image_height\": \"\",\n	".format(imgPath=params.imgPath)
    template += "\"content.category_teaser_image\": \"\",\n	\"content.category_teaser_image_width\": \"\",\n	\"content.category_teaser_image_height\": \"\",\n	"
    template += "\"template.show_alpha_index\": \"0\",\n	\"template.category_show\": \"1\",\n	\"template.category_subtitle\": \"1\",\n	"
    template += "\"template.category_teaser_text\": \"1\",\n	\"template.category_image\": \"1\",\n	"
    template += "\"template.category_text\": \"1\",\n	\"template.subcategory_show\": \"1\",\n	\"template.subcategory_teaser_text\": \"1\",\n	"
    template += "\"template.subcategory_teaser_image\": \"1\",\n	\"template.subcategory_empty\": \"1\",\n	\"template.item_pagination\": \"1\",\n	"
    template += "\"template.lastmodified\": \"1520231227\",\n	\"metadata.title\": \"{title}\",\n	\"metadata.description\": \"{description}\",\n	".format(title=params.title, description=params.description)
    template += "\"metadata.keywords\": \"\",\n	\"metadata.robots\": \"\",\n	\"metadata.author\": \"\"\n}');"   
    aliasCount+=1
    return template

class ItemParams:
    def __init__(self, id, appId, type, name, alias, content, title, desc, prCateg):
        self.id = id
        self.appId = appId
        self.type = type
        self.name = name
        self.alias = alias
        self.content = content
        self.title = title
        self.desc = desc
        self.prCateg = prCateg

itemDescId = "703f287e-3b84-46f2-add9-c3de16a78fca"


def GetItemTemplate(prefix, params):
    global aliasCount
    template = "INSERT INTO `{pref}_zoo_item` (`id`, `application_id`, `type`, `name`, `alias`, `created`, `modified`, `modified_by`, `publish_up`, `publish_down`, `priority`, `hits`, `state`, `access`, `created_by`, `created_by_alias`, `searchable`, `elements`, `params`) VALUES".format(pref=prefix)
    template += "({id}, {appId}, '{type}', '{name}', '{alias}', '2018-03-05 07:02:34', '2018-03-05 07:06:21', 145, '2018-03-05 07:02:34', '0000-00-00 00:00:00', 0, 1, 1, 1, 145, '', 1, ".format(id=params.id, appId=params.appId, type=params.type, name=params.name, alias=params.alias+str(aliasCount))
    template += '\'{ "'+itemDescId+'": {"0": {"value": "'+re.sub(r'((<a[^>]*>)|(</a>))', '', params.content)+'"}}}\', \n'
    template += "'{\n	\"metadata.title\": \""+params.title+"\", \n \"metadata.description\": \""+params.desc+"\", \n \"metadata.keywords\": \"\", \n \"metadata.robots\": \"\", \n \"metadata.author\": \"\", \n \"config.enable_comments\": \"1\", \n \"config.primary_category\": \""+str(params.prCateg)+"\"}' \n );"
    aliasCount+=1
    return template

def GetItemCatLinkTemplate(prefix, catId, itemId):
    template = "INSERT INTO `{pref}_zoo_category_item` (`category_id`, `item_id`) VALUES({catId}, {itemId});".format(pref=prefix, catId=catId, itemId=itemId)
    return template