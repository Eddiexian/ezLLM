<template>
    <div v-if="loading" class="loader"></div>
    <div class="container-fluid d-flex align-items-center justify-content-center">.
        <div v-if="loading" class="loader"></div>
        <div class="chat-dialog">
            <div class="chat-header">
                <h3 @click="getEmbedding">ChatGPT Q&A</h3>
                <button @click="readPDF">ReadPDF</button>
            </div>
            <div class="chat-body">
                <span @click="historyMode = !historyMode">HistoryMode : {{ historyMode }}</span>
                <div v-if="loading" class="thinking-message">GPT is thinking now...</div> <!-- 新增 -->
                <div v-for="(message, index) in messages" :key="index" class="chat-message">
                    <div :class="{ 'user-message': message.role == 'user', 'bot-message': message.role != 'user' }"
                        v-html="message.content">

                    </div>
                </div>

            </div>

            <div class="chat-footer">
                <input v-model="userInput" @keyup.enter="sendMessage('your name is yxma')"
                    placeholder="Type your question..." />
                <button @click="GetAns">Send</button>
            </div>
        </div>

    </div>

</template>
<script>
import axios from 'axios';
import * as pdfjsLib from 'pdfjs-dist';
pdfjsLib.GlobalWorkerOptions.workerSrc = '../../../node_modules/pdfjs-dist/build/pdf.worker.mjs'
// pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.7.76/build/pdf.worker.min.js';
export default {
    data() {
        return {
            loading: false,
            userInput: '',
            messages: [],
            historyMode: true,
            documentData: [],
        };
    },
    methods: {
        async loadModel() {

            try {
                const response = await axios.post('http://10.96.45.146:11434/api/generate', {
                    model: "taide"
                }, {

                });

                // 检查是否成功加载模型
                if (response.data.success) { // 假设API返回成功状态
                    this.modelLoaded = true;
                    console.log('Model loaded successfully');
                } else {
                    console.error('Failed to load model');
                }
            } catch (error) {
                console.error('Error loading model:', error);
                // 处理加载模型时的错误
            }
        },

        calculateSimilarity(embeddingA, embeddingB) {
            // 這裡可以用餘弦相似度或其他方法來計算相似度
            // 示例：計算餘弦相似度
            const dotProduct = embeddingA.reduce((sum, a, i) => sum + a * embeddingB[i], 0);
            const magnitudeA = Math.sqrt(embeddingA.reduce((sum, a) => sum + a * a, 0));
            const magnitudeB = Math.sqrt(embeddingB.reduce((sum, b) => sum + b * b, 0));
            return dotProduct / (magnitudeA * magnitudeB);
        },

        async sendMessage(rag_src) {
            // if (!this.userInput.trim()) return;

            // // 添加用户输入消息到消息数组
            // this.messages.push({
            //     role: "user",
            //     content: this.userInput
            // });
            // this.loading = true;

            // var messageAsk = {
            //     role: "user",
            //     content: this.userInput
            // }

            // if (this.historyMode) {
            //     messageAsk = this.messages
            // }

            // const documentList = await this.createDocumentListFromPdf("http://tw100039277.corpnet.auo.com/yx/CD.pdf", 300)

            // const queryEmbedding = await this.getEmbedding(this.userInput);
            // console.log(documentList)
            // const similarities = await Promise.all(documentList.map(async doc => {
            //     const docEmbedding = await this.getEmbedding(doc.text); // 獲取段落的嵌入
            //     return {
            //         text: doc.text,
            //         similarity: this.calculateSimilarity(queryEmbedding, docEmbedding),
            //     };
            // }));

            // similarities.sort((a, b) => b.similarity - a.similarity);

            // // 選擇前 n 個最相似的文本
            // const topDocs = similarities.slice(0, 5); // 例如：取前5個
            // // 將所有文本連接到 content 中
            // const content = topDocs.map(doc => doc.text).join('\n'); // 可以使用換行符號來分隔每段文本

            // messageAsk.push({
            //     role: "system",
            //     content: "請參考以下內容進行回答:\n" + content // 在前面添加提示信息
            // });


            // 调用Ollama GPT API
            try {
                const response = await axios.post('http://10.96.45.146:11434/api/chat',
                    {
                        'model': 'breeze',
                        'messages': [
                            { 'role': 'system', 'content': '請參考以下內容進行回答:\n我的名字是馬耀賢，是一位程式設計師' },
                            { 'role': 'user', 'content': '馬耀賢?' }
                        ],
                        'stream': false
                    }
                );

                // 打印完整的响应以便调试
                console.log('Response from API:', response.data);

                // 检查返回的消息
                if (response.data) {



                    const botMessage = response.data.message.content; // 获取机器人的回复
                    this.messages.push(response.data.message);


                } else {
                    this.messages.push({ content: 'No response from bot', role: 'info' });
                }

            } catch (error) {
                console.error('Error fetching data:', error);
                this.messages.push({ content: 'No response from bot', role: 'info' });
            } finally {
                this.loading = false;
                this.userInput = ''; // 清空输入框
            }
        },


        async readPDF() {
            const documentList = await this.createDocumentListFromPdf("http://tw100039277.corpnet.auo.com/yx/CD.pdf", 50)

            const queryEmbedding = await this.getEmbedding(this.userInput);
            console.log(documentList)
            await Promise.all(documentList.map(async doc => {
                const docEmbedding = await this.getEmbedding(doc.text); // 獲取段落的嵌入

                this.getEmbedding(doc.text)
      
            }));

        },

        async getEmbedding(text) {




            try {
                const response = await axios.post('http://10.96.45.146:6234/embed',

                    {

                        text: text,

                    }, {

                });

                // 打印完整的响应以便调试
                console.log('Response from API:', response.data);

                // 检查返回的消息
                if (response.data) {



                    return response.data



                } else {

                }

            } catch (error) {
                console.error('Error fetching data:', error);

            } finally {

            }
        },


        async GetAns() {
            try {
                const response = await axios.post('http://10.96.45.146:6234/rag',

                    {
                        query: "馬耀賢?",


                    }, {

                });

                // 打印完整的响应以便调试
                console.log('Response from API:', response.data);

                // 检查返回的消息
                if (response.data) {



                    return response.data.embedding



                } else {

                }

            } catch (error) {
                console.error('Error fetching data:', error);

            } finally {

            }

        },


        async getdb() {
            try {
                const response = await axios.get('http://10.96.45.146:6234/collections',

                );

                // 打印完整的响应以便调试
                console.log('Response from API:', response.data);

                // 检查返回的消息
                if (response.data) {



                    return response.data



                } else {

                }

            } catch (error) {
                console.error('Error fetching data:', error);

            } finally {

            }

        },
        async GetTags() {
            // 如果需要获取标签，您可以在这里实现
        },


        async readPdfAndSplitIntoSegments(pdfUrl, segmentSize) {
            const pdf = await pdfjsLib.getDocument(pdfUrl).promise;
            const numPages = pdf.numPages;
            let fullText = '';

            // 提取所有頁面的文本
            for (let pageNum = 1; pageNum <= numPages; pageNum++) {
                const page = await pdf.getPage(pageNum);
                const textContent = await page.getTextContent();
                const pageText = textContent.items.map(item => item.str).join(' '); // 提取文本
                fullText += ` ${pageText}`; // 加入段落，用空格分隔
            }

            // 分段
            const segments = this.splitTextIntoSegments(fullText, segmentSize);
            return segments;
        },

        splitTextIntoSegments(text, segmentSize) {
            const words = text.split(/\s+/); // 根據空格分詞
            const segments = [];

            for (let i = 0; i < words.length; i += segmentSize) {
                const segment = words.slice(i, i + segmentSize).join(" ");
                segments.push(segment);
            }

            return segments;
        },

        // 整理分段結果為所需格式
        async createDocumentListFromPdf(pdfUrl, segmentSize) {
            const segments = await this.readPdfAndSplitIntoSegments(pdfUrl, segmentSize);
            const documentList = segments.map(segment => ({ text: segment }));

            return documentList;
        }
    }
};
</script>

<style scoped>
.chat-dialog {
    width: 80vw;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.chat-header {
    background-color: #f5f5f5;
    padding: 10px;
    text-align: center;
}

.chat-body {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    background-color: #fff;
}

.chat-message {
    margin-bottom: 10px;
    white-space: pre-wrap;
}

.user-message {
    text-align: right;
    color: blue;
    white-space: pre-wrap;
}

.bot-message {
    text-align: left;
    color: green;
}

.chat-footer {
    display: flex;
    padding: 10px;
    background-color: #f5f5f5;
}

.chat-footer input {
    flex: 1;
    padding: 5px;
    margin-right: 5px;
}

.chat-footer button {
    padding: 5px 10px;
}

.thinking-message {
    text-align: center;
    color: orange;
    margin: 10px 0;
    font-style: italic;
}
</style>
