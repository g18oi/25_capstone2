from django.shortcuts import render

# Create your views here.
from stock.models import UserSurvey, CaregiverProfile

def calculate_match_score(user_survey, caregiver_profile):
    # 1. 활동 항목 유사도 (활동 리스트 교집합 비율)
    user_activities = set(user_survey.activities)
    caregiver_activities = set(caregiver_profile.activities)
    activity_score = len(user_activities.intersection(caregiver_activities)) / max(1, len(user_activities))

    # 2. 지역 매칭 (겹치는 지역 비율)
    user_regions = set(user_survey.hope_regions)
    caregiver_regions = set(caregiver_profile.regions)
    region_score = len(user_regions.intersection(caregiver_regions)) / max(1, len(user_regions))

    # 3. 시급 조건 (만족하면 1, 아니면 0)
    pay_score = 1 if caregiver_profile.hourly_pay >= user_survey.hope_pay else 0

    # 4. 정산 주기(월급, 주급 등) 조건 일치 여부
    pay_period_score = 1 if user_survey.pay_period in caregiver_profile.pay_periods else 0

    # 5. CCTV 동의 여부 일치 (둘 다 동의 or 둘 다 비동의)
    cctv_score = 1 if user_survey.cctv_agree == caregiver_profile.cctv_agree else 0

    # 가중치 합산 (예: 활동과 지역 중요하게 판단)
    total_score = (0.4 * activity_score +
                   0.3 * region_score +
                   0.1 * pay_score +
                   0.1 * pay_period_score +
                   0.1 * cctv_score)

    return total_score

def match_caregivers(request, survey_id):
    # 설문지 조회 시 예외 처리
    try:
        user_survey = UserSurvey.objects.get(id=survey_id)
    except UserSurvey.DoesNotExist:
        return render(request, 'error.html', {'message': '설문지를 찾을 수 없습니다.'})

    caregiver_qs = CaregiverProfile.objects.all()
    scored_caregivers = []

    for caregiver in caregiver_qs:
        # 리스트/배열 데이터 형식 보정(필요 시)
        user_activities = set(user_survey.activities if isinstance(user_survey.activities, list) else user_survey.activities.split(','))
        caregiver_activities = set(caregiver.activities if isinstance(caregiver.activities, list) else caregiver.activities.split(','))
        user_regions = set(user_survey.hope_regions if isinstance(user_survey.hope_regions, list) else user_survey.hope_regions.split(','))
        caregiver_regions = set(caregiver.region_list if isinstance(caregiver.region_list, list) else caregiver.region_list.split(','))

        score = calculate_match_score(user_survey, caregiver)
        scored_caregivers.append((caregiver, score))

    scored_caregivers.sort(key=lambda x: x[1], reverse=True)
    top_matches = scored_caregivers[:5]

    return render(request, 'matching_result.html', {
        'matches': top_matches,
        'user_survey': user_survey,
    })