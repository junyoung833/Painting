imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0]; // 업로드된 파일을 가져옵니다.
    if (!file) return; // 파일이 없으면 리턴합니다.

    const reader = new FileReader(); // 파일을 읽기 위한 FileReader 객체를 생성합니다.

    // 파일 읽기가 완료되었을 때 실행되는 함수입니다.
    reader.onload = () => {
        const img = new Image(); // 새로운 이미지 객체를 생성합니다.

        // 이미지 로드가 완료되면 캔버스에 그립니다.
        img.onload = () => {
            const x = canvas.width / 4; // 캔버스의 가로 중앙에서 약간 왼쪽으로 시작
            const y = canvas.height / 4; // 캔버스의 세로 중앙에서 약간 위쪽으로 시작
            const width = img.width / 2; // 이미지를 원본 크기의 절반으로 조정
            const height = img.height / 2; // 높이도 원본 크기의 절반으로 조정

            ctx.drawImage(img, x, y, width, height); // 캔버스에 이미지를 그립니다.
        };
        img.src = reader.result; // 파일 데이터로 이미지의 소스를 설정합니다.
    };

    reader.readAsDataURL(file); // 파일을 Data URL 형식으로 읽어옵니다.
});

