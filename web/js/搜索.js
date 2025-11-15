class 搜索框类 {
    constructor(搜索框ID = "文档搜索框") {
        this.搜索框元素 = document.getElementById(搜索框ID);
        this.搜索关键词 = "";
        this.当前任务 = null; // 用于存储当前搜索任务的 Promise 对象
        this.当前可取消的Promise = null; // 用于存储当前可取消的 Promise 对象

        if (!this.搜索框元素) {
            console.error(`未能找到 id 为 "${搜索框ID}" 的元素！`);
            return;
        }

        this.绑定事件();
    }

    // 绑定事件：监听回车按键和搜索框内容变化
    绑定事件() {
        this.搜索框元素.addEventListener('keydown', this.处理回车按键.bind(this));
        this.搜索框元素.addEventListener('input', this.处理搜索框内容变化.bind(this));
    }

    // 处理回车键按下事件
    async 处理回车按键(事件) {
        if (事件.key === "Enter") {
            this.搜索关键词 = this.搜索框元素.value.trim();

            // 如果搜索关键词为空，则不执行搜索
            if (!this.搜索关键词) {
                console.log('搜索关键词为空，不执行搜索');
                return;
            }

            console.log('输入关键词：', this.搜索关键词);
            // 执行搜索操作
            await this.执行搜索(this.搜索关键词);
        }
    }

    // 处理搜索框内容变化（清空时取消所有任务）
    处理搜索框内容变化(事件) {
        this.搜索关键词 = 事件.target.value.trim();

        // 如果搜索框内容为空，则取消所有任务并调用软更新
        if (!this.搜索关键词) {
            console.log('搜索关键词为空，取消所有任务');
            if (this.当前可取消的Promise) {
                if (typeof this.当前可取消的Promise.cancel === 'function') {
                    this.当前可取消的Promise.cancel();
                }
                this.当前可取消的Promise = null; // 清空当前可取消的 Promise
            }

            // 调用 window.app.条目填充.软更新(window.app.当前合集内容列表,false)
            window.app.条目填充.软更新(window.app.当前合集内容列表, false);
        }
    }

    // 执行搜索
    async 执行搜索(关键词) {
        // 创建一个可以取消的 Promise
        this.当前可取消的Promise = new Promise((resolve, reject) => {
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
                                    if (对象[键].includes(关键词)) {
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
                            if (字段 === 'id' || 字段 === 'uuid') {
                                // 对于 id 和 uuid 字段，使用 === 进行精确匹配
                                if (条目[字段] === 关键词) {
                                    精确匹配结果.push(条目);
                                    break; // 找到一个匹配的字段就跳出内循环
                                }
                            } else if (typeof 条目[字段] === 'string' && 条目[字段].includes(关键词)) {
                                // 对于其他字符串类型的字段，使用 includes 进行包含匹配
                                精确匹配结果.push(条目);
                                break; // 找到一个匹配的字段就跳出内循环
                            }
                        }
                    }
                }
                console.log('精确匹配结果：', 精确匹配结果);

                // 2. Jaro-Winkler 模糊匹配
                const jw匹配结果 = [];
                if (window.app.当前合集内容列表) {
                    for (const 条目 of window.app.当前合集内容列表) {
                        for (const 字段 in 条目) {
                            if (字段 === '文档内容' && typeof 条目[字段] === 'object' && 条目[字段] !== null) {
                                if (this.递归搜索(条目[字段], 关键词)) {
                                    jw匹配结果.push(条目);
                                    break;
                                }
                            } else if (typeof 条目[字段] === 'string') {
                                const 相似度是否匹配 = window.app.模糊算法.jaroWinkler距离(关键词, 条目[字段]);
                                if (相似度是否匹配 && !精确匹配结果.includes(条目)) {
                                    jw匹配结果.push(条目);
                                    break;
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
                        for (const 字段 in 条目) {
                            if (字段 === '文档内容' && typeof 条目[字段] === 'object' && 条目[字段] !== null) {
                                if (this.递归搜索(条目[字段], 关键词)) {
                                    编辑距离匹配结果.push(条目);
                                    break;
                                }
                            } else if (typeof 条目[字段] === 'string') {
                                const 编辑距离是否匹配 = window.app.模糊算法.编辑距离(关键词, 条目[字段]);
                                if (编辑距离是否匹配 && !精确匹配结果.includes(条目) && !jw匹配结果.includes(条目)) {
                                    编辑距离匹配结果.push(条目);
                                    break;
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
            window.app.条目填充.软更新(搜索结果, false);
            console.log('最终搜索结果：', 搜索结果);
            return 搜索结果;
        } catch (错误) {
            console.log('搜索被取消：', 错误.message);
            return null;
        }
    }

    // 递归搜索函数
    递归搜索(对象, 关键词) {
        for (const 键 in 对象) {
            if (typeof 对象[键] === 'string') {
                if (对象[键].includes(关键词)) {
                    return true; // 找到匹配项，返回 true
                }
            } else if (typeof 对象[键] === 'object' && 对象[键] !== null) {
                if (this.递归搜索(对象[键], 关键词)) {
                    return true; // 在子对象中找到匹配项，返回 true
                }
            }
        }
        return false; // 未找到匹配项，返回 false
    }
}
