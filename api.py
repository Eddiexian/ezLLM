from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import chromadb
from chromadb import Client
import os
from chromadb.config import Settings

app = Flask(__name__)

# 啟用 CORS
CORS(app)  # 這將允許所有來源的請求

# 設定持久化的資料夾
persist_directory = "db"
os.makedirs(persist_directory, exist_ok=True)
# 创建 Settings 实例，确保使用新配置
settings = Settings(
    is_persistent=True,  # 使能持久化
    persist_directory=persist_directory,  # 数据持久化的目录
    chroma_sysdb_impl="chromadb.db.impl.sqlite.SqliteDB",  # 使用新的系统数据库实现
    chroma_producer_impl="chromadb.db.impl.sqlite.SqliteDB",  # 数据生产者实现
    chroma_consumer_impl="chromadb.db.impl.sqlite.SqliteDB"   # 数据消费者实现
)

# 创建 Client 实例
client = Client(settings)

# 獲取現有集合
existing_collections = client.list_collections()
print("Existing collections:", existing_collections)

collection_name = "embedding_collection"
# if collection_name not in existing_collections:
#     collection = client.create_collection(collection_name)
#     print(f"Created collection: {collection_name}")
# else:
collection = client.get_collection(collection_name)
print(f"Using existing collection: {collection_name}")

# 假設 Ollama 的 Embedding API 是這個 URL
OLLAMA_EMBEDDING_URL = "http://10.96.45.146:11434/api/embeddings"

@app.route('/embed', methods=['POST'])
def embed():
    try:
        # 獲取 JSON 請求數據
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'No text provided.'}), 400
        
        text = data['text']
        print(text)
        # 呼叫 Ollama 的 Embedding API
        response = requests.post(OLLAMA_EMBEDDING_URL, json={"model": "breeze","prompt": text,})

        if response.status_code != 200:
            return jsonify({'error': 'Error calling Ollama API.'}), response.status_code

        # 假設 Ollama API 返回的 JSON 包含一個名為 "embedding" 的字段
        embedding = response.json().get("embedding")

        if embedding is None:
            return jsonify({'error': 'No embedding returned from Ollama API'}), 400

        # 為文檔生成一個 ID（可選）
        document_id = str(hash(text))  # 獲取文檔的唯一 ID，可以根據需要自定義生成方式

        # 將嵌入存儲到 Chroma
        # 增加 'ids' 參數
        collection.add(documents=[text], embeddings=[embedding], ids=[document_id])

        
        print(f"Stored document: {text} with ID: {document_id}")  # 調試日誌
        return jsonify({'message': 'Embedding stored successfully', 'embedding': embedding}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/collections', methods=['GET'])
def list_collections():
    collections = client.list_collections()
    collection_names = [col.name for col in collections]  # 提取集合名稱
    return jsonify(collection_names), 200

# 假設 Ollama 的 Chat API 是這個 URL
OLLAMA_CHAT_URL = "http://10.96.45.146:11434/api/chat"

@app.route('/rag', methods=['POST'])
def rag():
    try:
        # 獲取 JSON 請求數據
        data = request.get_json()
        if 'query' not in data:
            return jsonify({'error': 'No query provided.'}), 400
        
        user_query = data['query']

        # 使用查詢生成嵌入
        query_embedding = get_embedding(user_query)

        # 使用嵌入查詢相關文檔
        results = collection.query(query_embeddings=query_embedding, n_results=5)  # 請求最多 5 個

        # 提取相關文檔的內容
        related_docs = results['documents']  # 這裡獲取到的應該是 [[doc1], [doc2], ...]

        # 確保 related_docs 是一維的字符串列表
        flattened_docs = [doc for sublist in related_docs for doc in sublist]  # 展平文檔列表

        print("Flattened Query Results:", flattened_docs)  # 打印展平的查詢結果
        
        # 使用 Ollama 的 Chat API 獲得回答
        context = "\n".join(flattened_docs)  # 組合成一個上下文


        messageAsk = []
        
        messageAsk.append({"role": "system","content": "請參考以下內容進行回答:\n" + context})
        messageAsk.append({"role": "user","content": user_query})


        payload = {
            "model": "breeze",
                        "messages": messageAsk,
                        "stream": bool(0),
        }
        print(OLLAMA_CHAT_URL,payload)
        chat_response = requests.post(OLLAMA_CHAT_URL, json=payload)
        
        if chat_response.status_code != 200:
            return jsonify({'error': 'Error calling Ollama Chat API.'}), chat_response.status_code
        
        assistant_reply = chat_response.json()
        print(assistant_reply)
        return jsonify({
            'query': user_query,
            'message': assistant_reply,
            'related_documents': flattened_docs  # 返回展平的文檔列表
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_embedding(text):
    # 使用 Ollama 的 Embedding API 生成該文本的嵌入
    response = requests.post(OLLAMA_EMBEDDING_URL, json={"model": "breeze","prompt": text,})
    if response.status_code == 200:
        return response.json().get("embedding")
    else:
        raise Exception('Failed to get embedding')
    
@app.route('/documents', methods=['GET'])
def get_documents():
    collection_name = "embedding_collection"

    # 獲取集合
    collection = client.get_collection(collection_name)  # 直接獲取，避免使用 list_collections()

    if collection is None:
        return jsonify({'error': f'Collection {collection_name} does not exist.'}), 404
    
    # 查詢所有文檔
    results = collection.query(n_results=10)  # 查詢最多 10 條數據
    return jsonify(results), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6234)


