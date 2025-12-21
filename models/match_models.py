from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    # 역할 선택: 돌봄이용자(care_user), 돌봄선생님(care_teacher)
    USER_TYPE_CHOICES = [
        ('care_user', '돌봄이용자'),
        ('care_teacher', '돌봄선생님'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='care_user'
    )

class Care_Survey(models.Model):
    # 몇 명의 아이를 돌봐줄까요?
    CHILD_COUNT_CHOICES = [
        (1, '1명'),
        (2, '2명'),
    ]
    child_count = models.IntegerField(choices=CHILD_COUNT_CHOICES, default=1)
    
    # 아이1 정보
    child1_birth_year = models.PositiveIntegerField()
    child1_birth_month = models.PositiveIntegerField()
    
    # 아이2 정보 (optional)
    child2_birth_year = models.PositiveIntegerField(null=True, blank=True)
    child2_birth_month = models.PositiveIntegerField(null=True, blank=True)
    
    # 희망 시급
    hope_pay = models.PositiveIntegerField()
    negotiable = models.BooleanField(default=False)
    
    # 돌봄 서비스 종류 (복수 선택)
    CARE_TYPE_CHOICES = [
        ('indoor', '실내놀이'),
        ('pickup', '등하원 돕기'),
        ('english', '영어놀이'),
        ('korean', '한글놀이'),
        ('study', '학습지도'),
        ('outdoor', '야외활동'),
        ('meal', '밥 챙겨주기'),
        ('book', '책읽기'),
    ]
    care_types = models.JSONField(default=list)  # 복수 체크 지원
    
    # 추가요구사항
    extra_note = models.TextField(blank=True)

class TeacherSurvey(models.Model):
    # 가능한 활동 (다중 선택)
    ACTIVITY_CHOICES = [
        ('indoor', '구비된 장난감 실내놀이'),
        ('book', '책 읽어주기'),
        ('pickup', '등하원 동행'),
        ('meal', '밥 챙겨주기'),
        ('outdoor_near', '집 근처 야외 활동'),
        ('clean_up', '돌봄 후 뒷정리'),
        ('finance', '재우기/깨우기'),
        ('hygiene', '아이 위생 관리'),
        ('bath', '샤워/목욕/양치'),
        ('car_pickup', '자차로 등하원 시키기'),
        ('car_outdoor', '자차로 야외 활동'),
        ('postpartum', '산후 관리(산모, 신생아 건강관리)'),
        # 넣고싶은 활동 더 추가 가능
    ]
    activities = models.JSONField(default=list)  # 다중 체크
    # 희망 활동 지역 (최대 3곳)
    hope_regions = models.JSONField(default=list)  # 지역명 리스트
    # 희망 시급
    hope_pay = models.PositiveIntegerField()
    # 희망 정산 주기 (복수 선택)
    PAY_PERIOD_CHOICES = [
        ('weekly', '주급'),
        ('monthly', '월급'),
        ('daily', '일급'),
    ]
    pay_periods = models.JSONField(default=list)
    # CCTV 촬영 동의
    CCTV_CHOICES = [
        ('yes', 'CCTV가 있어도 괜찮아요'),
        ('no', 'CCTV 촬영을 원하지 않아요'),
    ]
    cctv_agree = models.CharField(max_length=10, choices=CCTV_CHOICES)
    # 추가로 희망하는 활동 영역
    extra_activities = models.TextField(blank=True)

#######
#데이터베이스관련 코드(삭제가능)
class UserSurvey(models.Model):
    activities = models.JSONField(default=list)
    hope_regions = models.JSONField(default=list)
    hope_pay = models.PositiveIntegerField()
    pay_period = models.CharField(max_length=50)
    cctv_agree = models.BooleanField()
    # 기타 필드 ...


#모든 돌봄선생님의 프로필을 가져옴
class CaregiverProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 정보 연동 필드
    activities = models.JSONField(default=list)
    regions = models.JSONField(default=list)
    hourly_pay = models.PositiveIntegerField()
    pay_periods = models.JSONField(default=list)
    cctv_agree = models.BooleanField()
    # 기타 필드 ...