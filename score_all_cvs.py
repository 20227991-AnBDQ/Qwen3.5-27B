import pandas as pd
import json
import requests

# ============================================
# RUBRIC: 7 TIÊU CHÍ CHẤM ĐIỂM
# ============================================

RUBRIC = {
    "academic": {
        "weight": 0.15,
        "name": "Thông tin nền tảng",
        "description": "GPA, trường, chuyên ngành"
    },
    "technical_skills": {
        "weight": 0.25,
        "name": "Kỹ năng kỹ thuật",
        "description": "Python, C++, TensorFlow, ROS, Git, Linux, Docker"
    },
    "projects": {
        "weight": 0.25,
        "name": "Project / Đồ án",
        "description": "Project AI/Robotics, Capstone, GitHub, vai trò rõ ràng"
    },
    "experience": {
        "weight": 0.15,
        "name": "Kinh nghiệm",
        "description": "Internship, Lab, RA/TA, CLB kỹ thuật, startup"
    },
    "achievements": {
        "weight": 0.10,
        "name": "Thành tích",
        "description": "Giải thưởng, Hackathon, Olympic, Publication, Học bổng"
    },
    "fit_position": {
        "weight": 0.05,
        "name": "Mức độ phù hợp AI/Robotics",
        "description": "Hướng AI/Robotics, giao thoa, match JD"
    },
    "potential": {
        "weight": 0.05,
        "name": "Tiềm năng phát triển",
        "description": "Tự học, chủ động, tư duy kỹ thuật, nghiêm túc"
    }
}

# ============================================
# HÀM CHẤM ĐIỂM CHI TIẾT
# ============================================

def score_academic(row):
    """Tiêu chí 1: Thông tin nền tảng (0-10)"""
    score = 0
    
    try:
        gpa = float(str(row['gpa']).replace(',', '.'))
        if gpa >= 3.8:
            score = 10
        elif gpa >= 3.6:
            score = 8
        elif gpa >= 3.4:
            score = 6
        elif gpa >= 3.0:
            score = 4
        else:
            score = 2
    except:
        score = 1
    
    return score

def score_technical_skills(row):
    """Tiêu chí 2: Kỹ năng kỹ thuật (0-10)"""
    score = 0
    skills = str(row['skills']).lower()
    
    # Ngôn ngữ lập trình (0-3)
    if 'python' in skills:
        score += 1
    if 'c++' in skills or 'c#' in skills:
        score += 1
    if 'java' in skills or 'c' in skills:
        score += 0.5
    
    # AI/ML frameworks (0-3)
    if 'pytorch' in skills:
        score += 1.5
    elif 'tensorflow' in skills or 'keras' in skills:
        score += 1
    if 'scikit-learn' in skills or 'sklearn' in skills:
        score += 0.5
    
    # Robotics (0-2)
    if 'ros' in skills or 'ros2' in skills:
        score += 1.5
    if 'opencv' in skills or 'slam' in skills or 'gazebo' in skills:
        score += 0.5
    
    # Công cụ (0-2)
    if 'git' in skills:
        score += 0.5
    if 'linux' in skills or 'docker' in skills:
        score += 0.5
    
    return min(score, 10)

def score_projects(row):
    """Tiêu chí 3: Project / Đồ án (0-10)"""
    score = 0
    projects = str(row['projects']).lower()
    
    # Project AI/Robotics (0-4)
    if 'ai' in projects or 'machine learning' in projects:
        score += 2
    if 'robot' in projects or 'robotics' in projects:
        score += 2
    
    # Capstone / Đồ án (0-2)
    if 'capstone' in projects or 'đồ án' in projects or 'thesis' in projects:
        score += 2
    
    # GitHub / Demo (0-2)
    if 'github' in projects or 'demo' in projects or 'repository' in projects:
        score += 2
    
    # Vai trò rõ ràng (0-2)
    if 'lead' in projects or 'leader' in projects or 'chủ nhiệm' in projects:
        score += 1
    if 'contributor' in projects or 'member' in projects or 'thành viên' in projects:
        score += 0.5
    
    return min(score, 10)

def score_experience(row):
    """Tiêu chí 4: Kinh nghiệm (0-10)"""
    score = 0
    experience = str(row['experience']).lower()
    
    # Internship (0-3)
    if 'internship' in experience or 'thực tập' in experience or 'intern' in experience:
        score += 3
    
    # Lab / Research (0-3)
    if 'lab' in experience or 'research' in experience or 'nghiên cứu' in experience:
        score += 3
    
    # RA/TA (0-2)
    if 'ra' in experience or 'ta' in experience or 'teaching' in experience:
        score += 2
    
    # CLB kỹ thuật / Startup (0-2)
    if 'club' in experience or 'clb' in experience or 'startup' in experience:
        score += 2
    
    return min(score, 10)

def score_achievements(row):
    """Tiêu chí 5: Thành tích (0-10)"""
    score = 0
    
    # Giải thưởng (0-3)
    if 'award' in str(row).lower() or 'giải' in str(row).lower():
        score += 3
    
    # Hackathon (0-2)
    if 'hackathon' in str(row).lower():
        score += 2
    
    # Olympic / Học thuật (0-2)
    if 'olympic' in str(row).lower() or 'competition' in str(row).lower():
        score += 2
    
    # Publication (0-2)
    if 'publication' in str(row).lower() or 'paper' in str(row).lower():
        score += 2
    
    # Học bổng (0-1)
    if 'scholarship' in str(row).lower() or 'học bổng' in str(row).lower():
        score += 1
    
    return min(score, 10)

def score_fit_position(row):
    """Tiêu chí 6: Mức độ phù hợp AI/Robotics (0-10)"""
    score = 0
    
    cv_text = (str(row['major']) + " " + str(row['skills']) + " " + str(row['projects'])).lower()
    
    # Hướng AI (0-3)
    if 'ai' in cv_text or 'machine learning' in cv_text or 'deep learning' in cv_text:
        score += 3
    
    # Hướng Robotics (0-3)
    if 'robot' in cv_text or 'robotics' in cv_text or 'automation' in cv_text:
        score += 3
    
    # Giao thoa AI + Robotics (0-4)
    if ('ai' in cv_text or 'ml' in cv_text) and ('robot' in cv_text or 'ros' in cv_text):
        score += 4
    
    return min(score, 10)

def score_potential(row):
    """Tiêu chí 7: Tiềm năng phát triển (0-10)"""
    score = 0
    
    cv_text = (str(row['major']) + " " + str(row['skills']) + " " + str(row['projects'])).lower()
    
    # Khả năng tự học (0-2)
    if 'self-taught' in cv_text or 'online course' in cv_text or 'mooc' in cv_text:
        score += 2
    
    # Chủ động (0-2)
    if 'initiative' in cv_text or 'proactive' in cv_text or 'chủ động' in cv_text:
        score += 2
    
    # Tư duy kỹ thuật (0-3)
    if 'problem solving' in cv_text or 'algorithm' in cv_text or 'optimization' in cv_text:
        score += 3
    
    # Khả năng đào tạo tiếp (0-2)
    if 'mentor' in cv_text or 'tutor' in cv_text or 'guide' in cv_text:
        score += 2
    
    # Mức độ nghiêm túc (0-1)
    if 'commitment' in cv_text or 'dedicated' in cv_text:
        score += 1
    
    return min(score, 10)

# ============================================
# HÀM CHẤM ĐIỂM TỔNG HỢP
# ============================================

def score_cv_comprehensive(row):
    """Chấm điểm CV theo 7 tiêu chí"""
    
    scores = {
        'academic': score_academic(row),
        'technical_skills': score_technical_skills(row),
        'projects': score_projects(row),
        'experience': score_experience(row),
        'achievements': score_achievements(row),
        'fit_position': score_fit_position(row),
        'potential': score_potential(row)
    }
    
    # Tính điểm tổng hợp (0-10)
    total_score = sum(scores[key] * RUBRIC[key]['weight'] for key in scores)
    
    return total_score, scores

def score_all_cvs():
    """Chấm điểm 500 CV theo rubric chi tiết"""
    
    print("="*70)
    print("📊 CHẤM ĐIỂM & XẾP HẠNG CV (7 TIÊU CHÍ)")
    print("="*70)
    
    # Đọc file CSV
    input_file = "data/cvs_normalized.csv"
    output_file = "data/cvs_scored.csv"
    
    print(f"\n📖 Đọc file: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Lỗi đọc file: {str(e)}")
        return
    
    print(f"✅ Tải {len(df)} CV\n")
    
    # Chấm điểm
    print("🔄 Chấm điểm theo 7 tiêu chí...")
    
    scores_list = []
    for idx, row in df.iterrows():
        total_score, detail_scores = score_cv_comprehensive(row)
        scores_list.append({
            'total_score': total_score,
            **detail_scores
        })
    
    # Thêm vào dataframe
    scores_df = pd.DataFrame(scores_list)
    df = pd.concat([df, scores_df], axis=1)
    
    # Xếp hạng
    print("🔄 Xếp hạng...")
    df['rank'] = df['total_score'].apply(
        lambda x: 'Shortlist' if x >= 7 else 'Borderline' if x >= 5 else 'Reject'
    )
    
    # Sắp xếp theo điểm giảm dần
    df = df.sort_values('total_score', ascending=False).reset_index(drop=True)
    
    # Lưu CSV
    print(f"\n💾 Lưu vào: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Thống kê
    print(f"\n✅ HOÀN THÀNH")
    print(f"\n📊 Thống kê:")
    print(f"  - Shortlist: {len(df[df['rank'] == 'Shortlist'])}")
    print(f"  - Borderline: {len(df[df['rank'] == 'Borderline'])}")
    print(f"  - Reject: {len(df[df['rank'] == 'Reject'])}")
    
    # Rubric
    print(f"\n📋 Rubric (Trọng số):")
    for key, value in RUBRIC.items():
        print(f"  {value['name']:30} ({value['weight']*100:5.1f}%)")
    
    # Top 10
    print(f"\n🏆 TOP 10 ỨNG VIÊN:")
    print("-"*70)
    
    top_10 = df[['name', 'major', 'total_score', 'rank']].head(10)
    
    for idx, row in top_10.iterrows():
        print(f"{idx+1:2}. {row['name'][:25]:25} | {row['major'][:15]:15} | {row['total_score']:5.1f} | {row['rank']}")
    
    # Top 5 shortlist chi tiết
    print(f"\n⭐ TOP 5 SHORTLIST (CHI TIẾT):")
    print("-"*70)
    
    shortlist = df[df['rank'] == 'Shortlist'].head(5)
    
    for idx, row in shortlist.iterrows():
        print(f"\n{idx+1}. {row['name']}")
        print(f"   Chuyên ngành: {row['major']}")
        print(f"   Kỹ năng: {row['skills']}")
        print(f"   Project: {row['projects']}")
        print(f"   Điểm tổng: {row['total_score']:.1f}/10")
        print(f"   Chi tiết:")
        print(f"     - Nền tảng: {row['academic']:.1f}")
        print(f"     - Kỹ năng kỹ thuật: {row['technical_skills']:.1f}")
        print(f"     - Project: {row['projects']:.1f}")
        print(f"     - Kinh nghiệm: {row['experience']:.1f}")
        print(f"     - Thành tích: {row['achievements']:.1f}")
        print(f"     - Phù hợp vị trí: {row['fit_position']:.1f}")
        print(f"     - Tiềm năng: {row['potential']:.1f}")

if __name__ == "__main__":
    score_all_cvs()
