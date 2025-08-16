// تابع کپی کردن شماره تلفن
function copyToClipboard(element) {
    const phoneNumber = element.textContent.trim();
    const tempInput = document.createElement('input');
    tempInput.value = phoneNumber;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    
    // نمایش اعلان کپی
    const copyNotice = element.querySelector('.copy-notice');
    copyNotice.style.opacity = '1';
    
    setTimeout(() => {
        copyNotice.style.opacity = '0';
    }, 2000);
}

// اضافه کردن event listener به تمام شماره‌های تلفن
document.addEventListener('DOMContentLoaded', function() {
    const phoneNumbers = document.querySelectorAll('.phone-number');
    phoneNumbers.forEach(number => {
        number.addEventListener('click', function() {
            copyToClipboard(this);
        });
    });
    
    // اسکرول افقی دسته‌بندی‌ها
    const categoriesScroll = document.querySelector('.categories-scroll');
    if (categoriesScroll) {
        let isDown = false;
        let startX;
        let scrollLeft;
        
        categoriesScroll.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - categoriesScroll.offsetLeft;
            scrollLeft = categoriesScroll.scrollLeft;
        });
        
        categoriesScroll.addEventListener('mouseleave', () => {
            isDown = false;
        });
        
        categoriesScroll.addEventListener('mouseup', () => {
            isDown = false;
        });
        
        categoriesScroll.addEventListener('mousemove', (e) => {
            if(!isDown) return;
            e.preventDefault();
            const x = e.pageX - categoriesScroll.offsetLeft;
            const walk = (x - startX) * 2;
            categoriesScroll.scrollLeft = scrollLeft - walk;
        });
    }
});
