from roles import add_role

sample_roles = [
    "Software Engineer",
    "Product Manager",
    "UX Designer",
    "Data Scientist",
    "Technical Recruiter"
]

if __name__ == "__main__":
    for role in sample_roles:
        result = add_role(role)
        print(f"{role}: {result['message']}")
