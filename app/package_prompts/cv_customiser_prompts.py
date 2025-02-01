
class CvPrompts:
    
    def get(self,*,job_description, cv_content, id=0):

        context_01=""" Act as a professional recruiter and CV 
                    specialist with expertise in [industry, e.g., tech, healthcare, engineering]. 
                    Your task is to optimize my existing CV to precisely match the 
                    requirements of the following job description:  """
        
        context_02 =""" Act as a professional recruiter and CV specialist. 
        Optimize the following CV to match the job requirements listed below."""

        cv_optimization_prompt = f"""
            {context_01}
        
        **Job Description**:
        {job_description}

        rrent CV Content**:
        {cv_content}

        **Instructions**:
        1. Use ATS-friendly keywords from the job description.
        2. Quantify achievements with metrics (e.g., "Increased sales by 30%").
        3. Align skills and experience with the job's core requirements.
        4. Return the optimized CV in markdown format.
        
        5. Add a "Changes Summary" section explaining key optimizations.
        """
        #4. Return the optimized CV in [HTML/DOCX-friendly plain text] format.

        match id:
            case 1:
                return cv_optimization_prompt
            case 2:
                return ""
        return "No prompt has found"