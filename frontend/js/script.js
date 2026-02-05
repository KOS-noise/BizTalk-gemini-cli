document.addEventListener('DOMContentLoaded', () => {
    const originalTextarea = document.getElementById('original-text');
    const charCountDisplay = document.getElementById('char-count');
    const convertBtn = document.getElementById('convert-btn');
    const targetSelect = document.getElementById('target-select');
    const resultDisplay = document.getElementById('result-text');
    const copyBtn = document.getElementById('copy-btn');
    const feedbackMsg = document.getElementById('feedback-msg');
    const btnText = convertBtn.querySelector('.btn-text');
    const spinner = convertBtn.querySelector('.spinner');
    const btnIcon = convertBtn.querySelector('svg');

    // 실시간 글자 수 세기
    originalTextarea.addEventListener('input', () => {
        const length = originalTextarea.value.length;
        charCountDisplay.textContent = `${length} / 500`;
        
        if (length > 0) {
            originalTextarea.classList.remove('error-border');
        }
    });

    // 말투 변환 함수
    async function convertText() {
        const text = originalTextarea.value.trim();
        const target = targetSelect.value;

        if (!text) {
            showFeedback('변환할 내용을 입력해주세요.', 'error');
            originalTextarea.classList.add('error-border');
            originalTextarea.focus();
            return;
        }

        // 로딩 상태 표시
        convertBtn.disabled = true;
        btnText.classList.add('hidden');
        btnIcon.classList.add('hidden');
        spinner.classList.remove('hidden');
        
        resultDisplay.textContent = '변환 중입니다...';
        resultDisplay.classList.add('result-placeholder');
        // Reset alignment classes for placeholder
        resultDisplay.classList.add('items-center', 'justify-center', 'text-center');
        resultDisplay.classList.remove('text-left', 'items-start');
        
        copyBtn.classList.add('hidden');
        hideFeedback();

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target }),
            });

            const data = await response.json();

            if (response.ok) {
                resultDisplay.textContent = data.converted_text;
                resultDisplay.classList.remove('result-placeholder', 'items-center', 'justify-center', 'text-center');
                resultDisplay.classList.add('text-left', 'items-start', 'text-slate-800');
                copyBtn.classList.remove('hidden');
            } else {
                throw new Error(data.error || '변환 중 오류가 발생했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            resultDisplay.textContent = '변환에 실패했습니다. 다시 시도해주세요.';
            showFeedback(error.message, 'error');
        } finally {
            // 로딩 상태 해제
            convertBtn.disabled = false;
            btnText.classList.remove('hidden');
            btnIcon.classList.remove('hidden');
            spinner.classList.add('hidden');
        }
    }

    // 복사 기능
    async function copyToClipboard() {
        const textToCopy = resultDisplay.textContent;
        
        try {
            await navigator.clipboard.writeText(textToCopy);
            showFeedback('클립보드에 복사되었습니다!', 'success');
            
            // 버튼 텍스트 일시적 변경
            const originalBtnText = copyBtn.textContent;
            copyBtn.textContent = '복사 완료!';
            setTimeout(() => {
                copyBtn.textContent = originalBtnText;
            }, 2000);
        } catch (err) {
            console.error('Copy failed:', err);
            showFeedback('복사 중 오류가 발생했습니다.', 'error');
        }
    }

    // 피드백 메시지 표시
    function showFeedback(message, type) {
        feedbackMsg.textContent = message;
        feedbackMsg.className = `hidden mt-4 p-4 rounded-xl text-sm font-medium text-center transition-all feedback-msg ${type}`;
        feedbackMsg.classList.remove('hidden');
    }

    function hideFeedback() {
        feedbackMsg.classList.add('hidden');
    }

    // 이벤트 리스너 등록
    convertBtn.addEventListener('click', convertText);
    copyBtn.addEventListener('click', copyToClipboard);
});
