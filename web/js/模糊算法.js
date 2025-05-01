// window.app = window.app || {};
const 模糊算法 = {
    默认JaroWinkler阈值: 0.8, // Jaro-Winkler 默认阈值 (更严格)

    jaroWinkler距离: function(字符串1, 字符串2, 阈值) {
        // Jaro-Winkler 距离算法实现
        if (字符串1 === 字符串2) return 1;

        let 长度1 = 字符串1.length,
            长度2 = 字符串2.length;
        if (长度1 === 0 || 长度2 === 0) return 0;

        let 匹配距离 = Math.floor(Math.max(长度1, 长度2) / 2) - 1;

        let 匹配1 = new Array(长度1),
            匹配2 = new Array(长度2);

        let 匹配数 = 0,
            换位数 = 0;

        for (let i = 0; i < 长度1; i++) {
            let 开始 = Math.max(0, i - 匹配距离);
            let 结束 = Math.min(长度2 - 1, i + 匹配距离);

            for (let j = 开始; j <= 结束; j++) {
                if (匹配2[j] || 字符串1[i] !== 字符串2[j]) continue;
                匹配1[i] = true;
                匹配2[j] = true;
                匹配数++;
                break;
            }
        }

        if (匹配数 === 0) return 0;

        let k = 0;
        for (let i = 0; i < 长度1; i++) {
            if (!匹配1[i]) continue;
            while (!匹配2[k]) k++;
            if (字符串1[i] !== 字符串2[k]) 换位数++;
            k++;
        }

        let jaro = (匹配数 / 长度1 + 匹配数 / 长度2 + (匹配数 - 换位数 / 2) / 匹配数) / 3;

        let 前缀 = 0,
            最大前缀 = 4;
        for (let i = 0; i < Math.min(长度1, 长度2, 最大前缀); i++) {
            if (字符串1[i] === 字符串2[i]) 前缀++;
            else break;
        }

        const 相似度 = jaro + 前缀 * 0.1 * (1 - jaro);
        阈值 = 阈值 || window.app.模糊算法.默认JaroWinkler阈值; // 优先使用传入的阈值，否则使用默认值
        return 相似度 >= 阈值; // 根据阈值判断是否匹配
    },

    编辑距离: function(字符串1, 字符串2, 阈值) {
        // 编辑距离算法实现
        const 长度1 = 字符串1.length;
        const 长度2 = 字符串2.length;
        const dp = Array(长度1 + 1).fill(null).map(() => Array(长度2 + 1).fill(0));

        for (let i = 0; i <= 长度1; i++) {
            dp[i][0] = i;
        }
        for (let j = 0; j <= 长度2; j++) {
            dp[0][j] = j;
        }

        for (let i = 1; i <= 长度1; i++) {
            for (let j = 1; j <= 长度2; j++) {
                if (字符串1[i - 1] === 字符串2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j],    // 删除
                        dp[i][j - 1],    // 插入
                        dp[i - 1][j - 1] // 替换
                    );
                }
            }
        }

        const 距离 = dp[长度1][长度2];

        // 根据字符串长度和是否包含中文动态调整阈值
        let 动态阈值;
        const 包含中文 = /[\u4e00-\u9fa5]/.test(字符串1 + 字符串2); // 检查是否包含中文

        if (包含中文) {
            动态阈值 = Math.max(1, Math.floor(Math.max(长度1, 长度2) / 3)); //中文阈值
        } else {
            动态阈值 = Math.max(1, Math.floor(Math.max(长度1, 长度2) / 5)); //英文阈值
        }

        // 如果没有传入阈值，则使用动态阈值
        阈值 = (阈值 === undefined || 阈值 === null) ? 动态阈值 : Math.min(阈值, 动态阈值);

        return 距离 <= 阈值; // 根据阈值判断是否匹配
    }
};
