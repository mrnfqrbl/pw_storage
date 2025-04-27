/**
 * 显示水印提示信息。
 *
 * @param {string} 消息 - 要显示的消息。
 */
function 显示水印提示(消息) {
    // 创建水印元素
    const 水印元素 = document.createElement('div');
    水印元素.style.position = 'fixed';
    水印元素.style.top = '50%';
    水印元素.style.left = '50%';
    水印元素.style.transform = 'translate(-50%, -50%)';
    水印元素.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    水印元素.style.color = 'white';
    水印元素.style.padding = '10px 20px';
    水印元素.style.borderRadius = '5px';
    水印元素.style.zIndex = '9999'; // 确保在其他元素之上
    水印元素.style.fontSize = '16px';
    水印元素.textContent = 消息;

    // 将水印元素添加到 body 中
    document.body.appendChild(水印元素);

    // 2 秒后移除水印元素
    setTimeout(() => {
        document.body.removeChild(水印元素);
    }, 2000);
}

// 导出函数，以便其他模块可以使用
window.水印提示=  显示水印提示;
