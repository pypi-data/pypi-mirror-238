import requests


def create_general_post(env,headers,platform,title,patternModel):
    """创建贴文，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    """
    url = "%s/api/posts/post/sales/create"%env
    data = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel
         }
    response = requests.post(url,headers=headers,json=data).json()
    print(response)
    sales_id = response["data"]["id"]
    return response,sales_id

def create_commerce_post(env,headers,platform,title,patternModel):
    """创建贴文，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    """
    url = "%s/api/posts/post/sales/create"%env
    data = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel,
      "postSubType": "COMMERCE_STACK"
         }
    response = requests.post(url,headers=headers,json=data).json()
    # print(response)
    sales_id = response["data"]["id"]
    return response,sales_id


if __name__=="__main__":
    # env = "https://front-admin.shoplineapp.com"
    # headers = {"Content-Type":"application/json","authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3YjdiM2E1MzU4M2IwYzlhZGVhODkyZDY3OTJlNTNlMSIsImRhdGEiOnsibWVyY2hhbnRfaWQiOiI2MWIwOTZiZWI3YmVmMTAwMjQ1ZGJkOGIiLCJhcHBsaWNhdGlvbl9pZCI6IjYyN2M3NTBhMDYyMzcwMDAwYWZlNWVmZCJ9LCJpc3MiOiJodHRwczovL2RldmVsb3BlcnMuc2hvcGxpbmVhcHAuY29tIiwiYXVkIjpbXSwic3ViIjoiNjFiMDk2YmViN2JlZjEwMDI0NWRiZDhiIn0.mkq54BMp-20y8oiw0qc9caeUzH-vT6oRkeUCpZrt1jI ","lang":"en"}
    # title = "jjjffff"
    # platform = "FACEBOOK"
    # patternModel = "EXACT_MATCH"
    # res,sales_id = create_general_post(env, headers, platform, title, patternModel)
    # print(res,sales_id)
    a = "新增自定义内容标题1698918524"
    a_list =['新增自定义内容标题1698918833', '新增自定义内容标题1698918797', '新增自定义内容标题1698918524', '新增自定义内容标题1698918300', '新增自定义内容标题1698918056', '新增自定义内容标题1698917855', '自定义内容标题1698914699']
    print(a in a_list )