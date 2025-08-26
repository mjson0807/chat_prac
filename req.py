import subprocess

def export_top_level_requirements(filename="requirements.txt"):
    # pip list --not-required 를 freeze 형태로 실행
    result = subprocess.run(
        ["pip", "list", "--not-required", "--format=freeze"],
        capture_output=True,
        text=True
    )
    
    # 결과를 파일로 저장
    with open(filename, "w") as f:
        f.write(result.stdout)
    
    print(f"✅ {filename} 에 top-level 패키지들이 저장되었습니다.")

# 실행
export_top_level_requirements()