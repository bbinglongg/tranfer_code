from langchain.llms import OpenAI

# 使用你的 Azure GPT-3 API 密钥
api_key = '你的API密钥'

# 初始化 OpenAI LLM (大型语言模型)
llm = OpenAI(api_key=api_key)

# 创建一个请求
prompt = "翻译这句话：Hello, world!"
response = llm(prompt)

# 打印响应
print(response)
