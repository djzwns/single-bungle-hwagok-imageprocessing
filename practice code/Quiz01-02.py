# 변수 선언
score, grade = 0, ''

# 메인
if __name__ == "__main__":
    score = int(input("성적 입력: "))
    
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(grade)
