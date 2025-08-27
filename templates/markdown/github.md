# {{ personal_info.name }}
## {{ personal_info.title }}

📍 {{ personal_info.location.city }}, {{ personal_info.location.state }}, {{ personal_info.location.country }}{% if personal_info.location.remote_friendly %} | 🌐 Remote Friendly{% endif %}  
📧 {{ personal_info.email }}{% if personal_info.phone %}  
📞 {{ personal_info.phone | format_phone }}{% endif %}

{% if personal_info.links %}
### 🔗 Links
{% if personal_info.links.linkedin %}[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({{ personal_info.links.linkedin }}){% endif %}
{% if personal_info.links.github %}[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({{ personal_info.links.github }}){% endif %}
{% if personal_info.links.website %}[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)]({{ personal_info.links.website }}){% endif %}
{% if personal_info.links.blog %}[![Blog](https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)]({{ personal_info.links.blog }}){% endif %}

{% endif %}
---

## 🎯 Professional Summary

{{ professional_summary.overview | replace('\n', '\n\n') }}

{% if professional_summary.key_strengths %}
### 💪 Key Strengths
{% for strength in professional_summary.key_strengths %}
- **{{ strength }}**
{% endfor %}
{% endif %}

**Experience:** {{ professional_summary.years_experience }} years

---

## 💼 Professional Experience

{% for exp in experience %}
### {{ exp.role }} @ **{{ exp.company }}**
*{{ exp.start_date | format_date }}{% if exp.end_date %} - {{ exp.end_date | format_date }}{% else %} - Present{% endif %}* | {{ exp.location or 'Location not specified' }}{% if exp.start_date and exp.end_date != exp.start_date %} | *{{ exp.start_date | format_duration(exp.end_date) }}*{% endif %}

{% if exp.company_description %}
> {{ exp.company_description }}
{% endif %}

{% if exp.achievements %}
{% for achievement in exp.achievements %}
- {{ achievement.description }}{% if achievement.metrics %} ({% for metric in achievement.metrics %}{{ metric.value }}{{ metric.unit }}{% if not loop.last %}, {% endif %}{% endfor %}){% endif %}
{% endfor %}
{% endif %}

{% if exp.achievements and exp.achievements|selectattr('technologies')|list %}
**Technologies:** {% for achievement in exp.achievements if achievement.technologies %}{% for tech in achievement.technologies %}`{{ tech }}`{% if not loop.last %} • {% endif %}{% endfor %}{% if not loop.last %} • {% endif %}{% endfor %}
{% endif %}

---
{% endfor %}

## 🛠️ Technical Skills

{% for category_name, category in skills.categories.items() %}
### {{ category.display_name }}
{% for skill in category.skills %}
{{ skill | skill_badge }}{% if not loop.last %} {% endif %}{% endfor %}

{% endfor %}

---

## 🎓 Education

{% for edu in education %}
### {{ edu.degree }} in {{ edu.field }}
**{{ edu.institution }}** | {{ edu.graduation_year }}{% if edu.location %} | {{ edu.location }}{% endif %}

{% if edu.gpa %}**GPA:** {{ edu.gpa }}{% endif %}
{% if edu.honors %}**Honors:** {{ edu.honors | join(', ') }}{% endif %}
{% if edu.relevant_coursework %}**Relevant Coursework:** {{ edu.relevant_coursework | join(', ') }}{% endif %}

{% endfor %}

{% if certifications %}
---

## 🏆 Certifications

{% for cert in certifications %}
- **{{ cert.name }}** | {{ cert.issuer }}{% if cert.issue_date %} | {{ cert.issue_date | format_date }}{% endif %}{% if cert.expiry_date %} - {{ cert.expiry_date | format_date }}{% endif %}
  {% if cert.credential_id %}*Credential ID: {{ cert.credential_id }}*{% endif %}
{% endfor %}
{% endif %}

{% if projects %}
---

## 🚀 Featured Projects

{% for project in projects %}
### {{ project.name }}
{{ project.description }}

**Status:** {{ project.status | title }}{% if project.start_date %} | **Timeline:** {{ project.start_date | format_date }}{% if project.end_date %} - {{ project.end_date | format_date }}{% endif %}{% endif %}

{% if project.technologies %}**Technologies:** {% for tech in project.technologies %}`{{ tech }}`{% if not loop.last %} • {% endif %}{% endfor %}{% endif %}

{% if project.url %}🔗 [Project Link]({{ project.url }}){% endif %}{% if project.github_url %}{% if project.url %} | {% endif %}📁 [GitHub]({{ project.github_url }}){% endif %}

---
{% endfor %}
{% endif %}

{% if awards %}
---

## 🏅 Awards & Recognition

{% for award in awards %}
- **{{ award.title }}** | {{ award.issuer }} | {{ award.date | format_date }}
  {% if award.description %}{{ award.description }}{% endif %}
{% endfor %}
{% endif %}

{% if publications %}
---

## 📚 Publications

{% for pub in publications %}
- **{{ pub.title }}** | *{{ pub.publication }}* | {{ pub.date | format_date }}
  {% if pub.url %}[Read Article]({{ pub.url }}){% endif %}
{% endfor %}
{% endif %}

{% if languages %}
---

## 🌍 Languages

{% for lang in languages %}
- **{{ lang.language }}**: {{ lang.proficiency | title }}
{% endfor %}
{% endif %}

---

<div align="center">

*This resume was generated using the [AI-Powered Resume System](https://github.com/silverbeer/tom-drake-resume) - Resume as Infrastructure*

**Last Updated:** {{ metadata.last_updated_formatted }} | **Built:** {{ metadata.build_date_formatted }}

</div>