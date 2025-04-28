const 搜索框对象 = {
    搜索框元素: null,
    搜索关键词: "",
    当前任务: null, // 用于存储当前搜索任务的 Promise 对象
    当前可取消的Promise: null, // 用于存储当前可取消的 Promise 对象
    初始化: function(搜索框ID) {
        搜索框ID = 搜索框ID || "文档搜索框";
        this.搜索框元素 = document.getElementById(搜索框ID);

        if (!this.搜索框元素) {
            console.error(`未能找到 id 为 "${搜索框ID}" 的元素！`);
            return;
        }

        this.绑定事件();
    },
    绑定事件: function() {
        this.搜索框元素.addEventListener('input', this.处理搜索.bind(this));
    },
    处理搜索: async function(事件) {
        this.搜索关键词 = 事件.target.value;

        // 立即 log 搜索关键词
        console.log('输入关键词：', this.搜索关键词);

        // 如果搜索框内容为空或空字符串，则取消所有任务并返回
        if (!this.搜索关键词 || this.搜索关键词.trim() === "") {
            console.log('搜索关键词为空，取消所有任务');
            if (this.当前可取消的Promise) {
                if (typeof this.当前可取消的Promise.cancel === 'function') {
                    this.当前可取消的Promise.cancel();
                }
                this.当前可取消的Promise = null; // 清空当前可取消的 Promise
            }

            // 调用 window.app.条目填充.软更新(window.app.当前合集内容列表,false)
            window.app.条目填充.软更新(window.app.当前合集内容列表, false);
            return; // 退出函数，不执行搜索
        }

        // 取消之前的任务 (如果存在)
        if (this.当前可取消的Promise) {
            if (typeof this.当前可取消的Promise.cancel === 'function') {
                this.当前可取消的Promise.cancel();
            }
        }

        // 立即执行搜索
        this.当前任务 = this.执行搜索(this.搜索关键词);
    },
    执行搜索: async function(关键词) {
        // 创建一个可以取消的 Promise
        this.当前可取消的Promise = new Promise((resolve, reject) => {
            // 将 reject 函数暴露给 Promise 对象，用于取消任务
            this.当前可取消的Promise.cancel = () => {
                reject(new Error('任务被取消'));
            };

            // 模拟搜索操作
            setTimeout(() => {
                console.log('执行搜索操作，关键词：', 关键词);

                // 1. 精确匹配
                const 精确匹配结果 = [];
                if (window.app.当前合集内容列表) {
                    for (const 条目 of window.app.当前合集内容列表) {
                        // 递归搜索函数
                        const 递归搜索 = (对象, 关键词) => {
                            for (const 键 in 对象) {
                                if (typeof 对象[键] === 'string') {
                                    console.log(`精确匹配（递归）：正在检查 对象[${键}] = ${对象[键]} 是否包含 关键词 = ${关键词}`);
                                    if (对象[键].includes(关键词)) {
                                        console.log(`精确匹配（递归）：找到匹配项，条目 = `, 条目);
                                        return true; // 找到匹配项，返回 true
                                    } else {
                                        console.log(`精确匹配（递归）：未找到匹配项`);
                                    }
                                } else if (typeof 对象[键] === 'object' && 对象[键] !== null) {
                                    // 如果是对象，则递归搜索
                                    if (递归搜索(对象[键], 关键词)) {
                                        return true; // 在子对象中找到匹配项，返回 true
                                    }
                                }
                            }
                            return false; // 未找到匹配项，返回 false
                        };

                        for (const 字段 in 条目) {
                            console.log(`精确匹配：正在检查 条目[${字段}] = ${条目[字段]} 是否 包含 关键词 = ${关键词}`);
                            if (字段 === 'id' || 字段 === 'uuid') {
                                // 对于 id 和 uuid 字段，使用 === 进行精确匹配
                                if (条目[字段] === 关键词) {
                                    console.log(`精确匹配：找到匹配项（id 或 uuid），条目 = `, 条目);
                                    精确匹配结果.push(条目);
                                    break; // 找到一个匹配的字段就跳出内循环
                                } else {
                                    console.log(`精确匹配：未找到匹配项（id 或 uuid）`);
                                }
                            } else if (字段 === '文档内容' && typeof 条目[字段] === 'object' && 条目[字段] !== null) {
                                // 如果是文档内容字典，则递归搜索
                                if (递归搜索(条目[字段], 关键词)) {
                                    精确匹配结果.push(条目);
                                    break; // 找到一个匹配的字段就跳出内循环
                                }
                            } else if (typeof 条目[字段] === 'string' && 条目[字段].includes(关键词)) {
                                // 对于其他字符串类型的字段，使用 includes 进行包含匹配
                                console.log(`精确匹配：找到匹配项，条目 = `, 条目);
                                精确匹配结果.push(条目);
                                break; // 找到一个匹配的字段就跳出内循环
                            } else {
                                console.log(`精确匹配：未找到匹配项`);
                            }
                        }
                    }
                }
                console.log('精确匹配结果：', 精确匹配结果);

                // 2. Jaro-Winkler 模糊匹配
                const jw匹配结果 = [];
                if (window.app.当前合集内容列表) {
                    for (const 条目 of window.app.当前合集内容列表) {
                        // 递归搜索函数
                        const 递归搜索 = (对象, 关键词) => {
                            for (const 键 in 对象) {
                                if (typeof 对象[键] === 'string') {
                                    const 相似度是否匹配 = window.app.模糊算法.jaroWinkler距离(关键词, 对象[键]);
                                    // console.log(`Jaro-Winkler 模糊匹配（递归）：关键词 = ${关键词}，对象[${键}] = ${对象[键]}，是否匹配 = ${相似度是否匹配}`);
                                    if (相似度是否匹配) {
                                        console.log(`Jaro-Winkler 模糊匹配（递归）：找到匹配项，条目 = `, 条目);
                                        return true; // 找到匹配项，返回 true
                                    }
                                } else if (typeof 对象[键] === 'object' && 对象[键] !== null) {
                                    // 如果是对象，则递归搜索
                                    if (递归搜索(对象[键], 关键词)) {
                                        return true; // 找到匹配项，返回 true
                                    }
                                }
                            }
                            return false; // 未找到匹配项，返回 false
                        };

                        for (const 字段 in 条目) {
                            if (字段 === '文档内容' && typeof 条目[字段] === 'object' && 条目[字段] !== null) {
                                // 如果是文档内容字典，则递归搜索
                                if (递归搜索(条目[字段], 关键词)) {
                                    jw匹配结果.push(条目);
                                    break; // 找到一个匹配的字段就跳出内循环
                                }
                            } else if (typeof 条目[字段] === 'string' && 字段 !== 'id' && 字段 !== 'uuid') {
                                // 排除 id 和 uuid 字段
                                const 相似度是否匹配 = window.app.模糊算法.jaroWinkler距离(关键词, 条目[字段]);
                                console.log(`Jaro-Winkler 模糊匹配：关键词 = ${关键词}，条目[${字段}] = ${条目[字段]}，是否匹配 = ${相似度是否匹配}`);
                                if (相似度是否匹配 && !精确匹配结果.includes(条目)) { // 排除精确匹配的结果
                                    console.log(`Jaro-Winkler 模糊匹配：找到匹配项，条目 = `, 条目);
                                    jw匹配结果.push(条目);
                                    break;
                                } else {
                                    console.log(`Jaro-Winkler 模糊匹配：未找到匹配项`);
                                }
                            }
                        }
                    }
                }
                console.log('Jaro-Winkler 匹配结果：', jw匹配结果);

                // 3. 编辑距离模糊匹配
                const 编辑距离匹配结果 = [];
                if (window.app.当前合集内容列表) {
                    for (const 条目 of window.app.当前合集内容列表) {
                        // 递归搜索函数
                        const 递归搜索 = (对象, 关键词) => {
                            for (const 键 in 对象) {
                                if (typeof 对象[键] === 'string') {
                                    const 编辑距离是否匹配 = window.app.模糊算法.编辑距离(关键词, 对象[键]);
                                    // console.log(`编辑距离模糊匹配（递归）：关键词 = ${关键词}，对象[${键}] = ${对象[键]}，是否匹配 = ${编辑距离是否匹配}`);
                                    if (编辑距离是否匹配) {
                                        console.log(`编辑距离模糊匹配（递归）：找到匹配项，条目 = `, 条目);
                                        return true; // 找到匹配项，返回 true
                                    }
                                } else if (typeof 对象[键] === 'object' && 对象[键] !== null) {
                                    // 如果是对象，则递归搜索
                                    if (递归搜索(对象[键], 关键词)) {
                                        return true; // 在子对象中找到匹配项，返回 true
                                    }
                                }
                            }
                            return false; // 未找到匹配项，返回 false
                        };

                        for (const 字段 in 条目) {
                            if (字段 === '文档内容' && typeof 条目[字段] === 'object' && 条目[字段] !== null) {
                                // 如果是文档内容字典，则递归搜索
                                if (递归搜索(条目[字段], 关键词)) {
                                    编辑距离匹配结果.push(条目);
                                    break; // 找到一个匹配的字段就跳出内循环
                                }
                            } else if (typeof 条目[字段] === 'string' && 字段 !== 'id' && 字段 !== 'uuid') {
                                // 排除 id 和 uuid 字段
                                const 编辑距离是否匹配 = window.app.模糊算法.编辑距离(关键词, 条目[字段]);
                                console.log(`编辑距离模糊匹配：关键词 = ${关键词}，条目[${字段}] = ${条目[字段]}，是否匹配 = ${编辑距离是否匹配}`);
                                if (编辑距离是否匹配 && !精确匹配结果.includes(条目) && !jw匹配结果.includes(条目)) { // 排除精确匹配和 Jaro-Winkler 匹配的结果
                                    console.log(`编辑距离模糊匹配：找到匹配项，条目 = `, 条目);
                                    编辑距离匹配结果.push(条目);
                                    break;
                                } else {
                                    console.log(`编辑距离模糊匹配：未找到匹配项`);
                                }
                            }
                        }
                    }
                }
                console.log('编辑距离匹配结果：', 编辑距离匹配结果);

                // 4. 组合结果并排序 (精确匹配 > Jaro-Winkler > 编辑距离)
                const 搜索结果 = [...精确匹配结果, ...jw匹配结果, ...编辑距离匹配结果];

                // 使用 Set 去重
                const 去重后的搜索结果 = [...new Set(搜索结果)];

                console.log('搜索结果：', 去重后的搜索结果);
                resolve(去重后的搜索结果);
            }, 500); // 模拟 500 毫秒的搜索延迟
        });

        try {
            const 搜索结果 = await this.当前可取消的Promise;
            window.app.条目填充.软更新(搜索结果,false)
            console.log('最终搜索结果：', 搜索结果);
            return 搜索结果;
        } catch (错误) {
            console.log('搜索被取消：', 错误.message);
            return null;
        }
    }
};

window.app.搜索框 = 搜索框对象;
