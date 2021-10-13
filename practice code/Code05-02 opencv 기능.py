# 얼룩말 교재 p121
import cv2

src = cv2.imread("../images/Nature99(Small)/picture01-2.jpg")
dst1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
dst2 = cv2.cvtColor(src, cv2.COLOR_BGRA2RGBA)
dst3 = cv2.cvtColor(dst1, cv2.COLOR_GRAY2RGB)
cv2.imshow("src", src)
cv2.imshow("gray", dst3)

cv2.waitKey(0)
cv2.destroyAllWindows()


"""
# 다음 미션 cv 전용 함수들 기존 코드에 추가 구현하기
# 추가로 메뉴도 만들어서 cv용 메뉴도 만들것
"""