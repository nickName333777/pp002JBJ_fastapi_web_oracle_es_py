console.log('signup.js loaded ...');

const API_BASE_URL = "http://localhost:8000";

// 유효성 검사 결과 객체
const checkObj = {
    memberEmail: false,
    memberPw: false,
    memberPwConfirm: false,
    memberName: false,
    memberNickname: false,
    memberTel: false,
    memberCareer: false,
    authKey: false
};

// 이메일 유효성 검사
const memberEmail = document.getElementById("memberEmail");
const emailMessage = document.getElementById("emailMessage");

memberEmail.addEventListener("input", async function() {
    if (memberEmail.value === "") {
        emailMessage.innerText = "메일을 받을 수 있는 이메일을 입력해주세요.";
        emailMessage.classList.remove("confirm", "error");
        checkObj.memberEmail = false;
        return;
    }
    
    const regExp = /^[\w\_.]{4,}@[a-z]+(\.[a-z]+){1,2}$/;
    
    if (regExp.test(memberEmail.value)) {
        try {
            const response = await fetch(`${API_BASE_URL}/member/dupcheck/email?email=${memberEmail.value}`);
            const data = await response.json();
            
            if (data.exists) {
                emailMessage.innerText = "이미 사용중인 이메일 입니다.";
                emailMessage.classList.add("error");
                emailMessage.classList.remove("confirm");
                checkObj.memberEmail = false;
            } else {
                emailMessage.innerText = "사용 가능한 이메일입니다.";
                emailMessage.classList.add("confirm");
                emailMessage.classList.remove("error");
                checkObj.memberEmail = true;
            }
        } catch (error) {
            console.error("이메일 중복 체크 오류:", error);
        }
    } else {
        emailMessage.innerText = "이메일 형식이 유효하지 않습니다.";
        emailMessage.classList.add("error");
        emailMessage.classList.remove("confirm");
        checkObj.memberEmail = false;
    }
});

// 인증번호 발송
let authTimer;
let authMin = 4;
let authSec = 59;
let tempEmail = "";

document.getElementById("sendAuthKeyBtn").addEventListener("click", async function() {
    if (!checkObj.memberEmail) {
        alert("유효한 이메일을 작성해주세요.");
        memberEmail.focus();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/sendEmail/signup?email=${memberEmail.value}`);
        const data = await response.json();
        
        if (data.result > 0) {
            tempEmail = memberEmail.value;
            alert("인증번호가 발송되었습니다.");
            
            authMin = 4;
            authSec = 59;
            authKeyMessage.innerText = "05:00";
            authKeyMessage.classList.remove("confirm");
            
            clearInterval(authTimer);
            
            authTimer = setInterval(() => {
                authKeyMessage.innerText = "0" + authMin + ":" + (authSec < 10 ? "0" + authSec : authSec);
                
                if (authMin === 0 && authSec === 0) {
                    checkObj.authKey = false;
                    clearInterval(authTimer);
                    return;
                }
                
                if (authSec === 0) {
                    authSec = 60;
                    authMin--;
                }
                
                authSec--;
            }, 1000);
        }
    } catch (error) {
        console.error("인증번호 발송 오류:", error);
        alert("인증번호 발송에 실패했습니다.");
    }
});

// 인증 확인
const authKey = document.getElementById("authKey");
const authKeyMessage = document.getElementById("authKeyMessage");

document.getElementById("checkAuthKeyBtn").addEventListener("click", async function() {
    if (authMin === 0 && authSec === 0) {
        alert("인증 시간이 만료되었습니다. 다시 시도해주세요.");
        return;
    }
    
    try {
        const response = await fetch(
            `${API_BASE_URL}/sendEmail/checkAuthKey?inputKey=${authKey.value}&email=${tempEmail}`
        );
        const data = await response.json();
        
        if (data.result > 0) {
            clearInterval(authTimer);
            authKeyMessage.innerText = "인증되었습니다.";
            authKeyMessage.classList.add("confirm");
            checkObj.authKey = true;
        } else {
            alert("인증번호가 일치하지 않습니다.");
            checkObj.authKey = false;
        }
    } catch (error) {
        console.error("인증 확인 오류:", error);
    }
});

// 비밀번호 유효성 검사
const memberPw = document.getElementById("memberPw");
const memberPwConfirm = document.getElementById("memberPwConfirm");
const pwMessage = document.getElementById("pwMessage");

memberPw.addEventListener("input", function() {
    if (memberPw.value.trim().length === 0) {
        pwMessage.innerText = "영어, 숫자, 특수문자(!, @, #, -, _) 6~20글자 사이로 입력해 주세요.";
        pwMessage.classList.remove("confirm", "error");
        checkObj.memberPw = false;
        return;
    }
    
    const regExp = /^[\w!@#\-_]{6,20}$/;
    
    if (regExp.test(memberPw.value)) {
        checkObj.memberPw = true;
        
        if (memberPwConfirm.value === "") {
            pwMessage.innerText = "사용가능한 비밀번호 입니다.";
            pwMessage.classList.add("confirm");
            pwMessage.classList.remove("error");
        } else {
            if (memberPw.value === memberPwConfirm.value) {
                pwMessage.innerText = "비밀번호가 일치합니다.";
                pwMessage.classList.add("confirm");
                pwMessage.classList.remove("error");
                checkObj.memberPwConfirm = true;
            } else {
                pwMessage.innerText = "비밀번호가 일치하지 않습니다.";
                pwMessage.classList.add("error");
                pwMessage.classList.remove("confirm");
                checkObj.memberPwConfirm = false;
            }
        }
    } else {
        pwMessage.innerText = "사용 불가능한 비밀번호 입니다.";
        pwMessage.classList.add("error");
        pwMessage.classList.remove("confirm");
        checkObj.memberPw = false;
    }
});

memberPwConfirm.addEventListener("input", () => {
    if (memberPw.value === "") {
        alert("비밀번호를 입력해주세요.");
        memberPwConfirm.value = "";
        memberPw.focus();
        return;
    }
    
    if (checkObj.memberPw) {
        if (memberPw.value === memberPwConfirm.value) {
            pwMessage.innerText = "비밀번호가 일치합니다.";
            pwMessage.classList.add("confirm");
            pwMessage.classList.remove("error");
            checkObj.memberPwConfirm = true;
        } else {
            pwMessage.innerText = "비밀번호가 일치하지 않습니다.";
            pwMessage.classList.add("error");
            pwMessage.classList.remove("confirm");
            checkObj.memberPwConfirm = false;
        }
    } else {
        checkObj.memberPwConfirm = false;
    }
});

// 이름, 닉네임, 전화번호, 경력사항 유효성 검사 (생략 - 패턴은 동일)
// ... (나머지 필드 검사 코드는 위와 동일한 패턴)

// 회원가입 폼 제출
document.getElementById("signUpFrm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // 모든 필드 검증
    for (let key in checkObj) {
        if (!checkObj[key]) {
            alert(`${key}가 유효하지 않습니다.`);
            document.getElementById(key)?.focus();
            return;
        }
    }
    
    const formData = {
        member_email: memberEmail.value,
        member_pw: memberPw.value,
        member_name: document.getElementById("memberName").value,
        member_nickname: document.getElementById("memberNickname").value,
        member_tel: document.getElementById("memberTel").value,
        member_career: document.getElementById("memberCareer").value,
        member_subscribe: document.getElementById("memberSubscribe").checked ? 'Y' : 'N'
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/member/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(data.message);
            window.location.href = '/login.html';
        } else {
            throw new Error(data.detail || '회원가입에 실패했습니다.');
        }
    } catch (error) {
        console.error("회원가입 오류:", error);
        alert(error.message);
    }
});
