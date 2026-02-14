"""Pre-built mock responses for demo safety.

If LLM fails during a live demo, these responses are used instead.
They represent a realistic analysis for a CS student targeting ML Engineer role.
"""

MOCK_ROADMAP_RESPONSE = {
    "skill_map": {
        "skills": [
            {"name": "Python", "level": "intermediate", "category": "technical"},
            {"name": "JavaScript", "level": "beginner", "category": "technical"},
            {"name": "HTML/CSS", "level": "intermediate", "category": "technical"},
            {"name": "Git", "level": "intermediate", "category": "tool"},
            {"name": "SQL", "level": "beginner", "category": "technical"},
            {"name": "React", "level": "beginner", "category": "technical"},
            {"name": "NumPy", "level": "beginner", "category": "tool"},
            {"name": "Communication", "level": "intermediate", "category": "soft"},
            {"name": "Problem Solving", "level": "intermediate", "category": "soft"},
            {"name": "Teamwork", "level": "advanced", "category": "soft"},
        ],
        "strengths": [
            "Solid Python foundation with project experience",
            "Good collaborative skills from group projects",
            "Curiosity-driven learner with diverse project portfolio",
        ],
        "weaknesses": [
            "No hands-on ML/DL project experience",
            "Weak mathematical foundations for ML (linear algebra, statistics)",
            "No experience with ML frameworks (PyTorch, TensorFlow, Scikit-learn)",
            "No exposure to ML ops or model deployment",
        ],
    },
    "role_requirements": {
        "core_technical": [
            "Python (advanced)",
            "PyTorch or TensorFlow",
            "Scikit-learn",
            "Data preprocessing pipelines",
            "Model training & evaluation",
            "Feature engineering",
        ],
        "supporting_skills": [
            "SQL for data querying",
            "Docker for containerization",
            "Git & version control",
            "REST API development",
            "Cloud platforms (AWS/GCP basics)",
        ],
        "theory_math": [
            "Linear algebra (vectors, matrices, eigenvalues)",
            "Probability & statistics",
            "Calculus (gradients, chain rule)",
            "Optimization (gradient descent)",
            "Information theory basics",
        ],
        "tools": [
            "Jupyter Notebooks",
            "MLflow or W&B for experiment tracking",
            "Pandas & NumPy",
            "Hugging Face Transformers",
            "Matplotlib/Seaborn for visualization",
        ],
        "soft_skills": [
            "Problem decomposition",
            "Technical writing & documentation",
            "Cross-functional collaboration",
            "Experiment design & hypothesis testing",
        ],
        "portfolio_expectations": [
            "At least one end-to-end ML project",
            "Model deployed as a REST API",
            "Kaggle competition participation",
            "Reproduced a research paper result",
        ],
    },
    "gap_analysis": {
        "critical": [
            {"skill": "PyTorch/TensorFlow", "reason": "Cannot build ML models without a deep learning framework — this is the #1 tool requirement for the role."},
            {"skill": "Scikit-learn", "reason": "Essential for classical ML tasks like classification, regression, and preprocessing."},
            {"skill": "Linear Algebra", "reason": "Foundational math for understanding how models work internally. Blocks deeper learning."},
            {"skill": "Model Training & Evaluation", "reason": "Core job function — must understand training loops, loss functions, and metrics."},
        ],
        "important": [
            {"skill": "Data Preprocessing", "reason": "80% of real ML work is data wrangling. Current SQL/Pandas skills are too shallow."},
            {"skill": "Probability & Statistics", "reason": "Needed for model evaluation, A/B testing, and understanding distributions."},
            {"skill": "Docker", "reason": "Standard for ML model deployment and reproducibility."},
            {"skill": "Experiment Tracking (MLflow/W&B)", "reason": "Professional ML workflows require systematic experimentation."},
        ],
        "nice_to_have": [
            {"skill": "Cloud Platforms (AWS/GCP)", "reason": "Useful for deployment but not critical at entry level."},
            {"skill": "Hugging Face Transformers", "reason": "Valuable for NLP roles but can be learned on the job."},
            {"skill": "Information Theory", "reason": "Deepens understanding but not immediately required."},
        ],
    },
    "roadmap": {
        "days": [
            {"day": 1, "objective": "Python for ML: NumPy mastery", "resource": "NumPy official quickstart + freeCodeCamp NumPy tutorial", "task": "Complete 20 NumPy array manipulation exercises", "output": "Jupyter notebook with exercises", "hours": 3},
            {"day": 2, "objective": "Pandas for data wrangling", "resource": "Kaggle Pandas micro-course", "task": "Load, clean, and analyze a CSV dataset", "output": "Cleaned dataset + analysis notebook", "hours": 3},
            {"day": 3, "objective": "Data visualization fundamentals", "resource": "Matplotlib & Seaborn tutorial (Real Python)", "task": "Create 5 different chart types from a dataset", "output": "Visualization notebook", "hours": 2.5},
            {"day": 4, "objective": "Linear algebra: Vectors & matrices", "resource": "3Blue1Brown Essence of Linear Algebra (Ep 1-4)", "task": "Hand-solve 10 matrix operations, implement in NumPy", "output": "Math notebook with NumPy verification", "hours": 3},
            {"day": 5, "objective": "Linear algebra: Transformations & eigenvalues", "resource": "3Blue1Brown (Ep 5-8) + Khan Academy exercises", "task": "Visualize 2D transformations with matplotlib", "output": "Transformation visualization script", "hours": 3},
            {"day": 6, "objective": "Statistics fundamentals", "resource": "StatQuest: Histograms, Mean, Variance, Std Dev", "task": "Compute stats on a real dataset, interpret results", "output": "Statistical analysis notebook", "hours": 2.5},
            {"day": 7, "objective": "Week 1 review + mini-project", "resource": "Kaggle Titanic dataset", "task": "EDA on Titanic: clean, visualize, find patterns", "output": "Complete EDA notebook (portfolio piece #1)", "hours": 4},
            {"day": 8, "objective": "Intro to Scikit-learn", "resource": "Scikit-learn official tutorial: Getting Started", "task": "Train your first classifier on Iris dataset", "output": "Working classification notebook", "hours": 3},
            {"day": 9, "objective": "Supervised learning: Regression", "resource": "Scikit-learn regression tutorial + StatQuest", "task": "Build a housing price predictor", "output": "Regression model with evaluation metrics", "hours": 3},
            {"day": 10, "objective": "Supervised learning: Classification", "resource": "Scikit-learn classification guide", "task": "Build a spam classifier with multiple algorithms", "output": "Comparison notebook with accuracy scores", "hours": 3},
            {"day": 11, "objective": "Model evaluation & validation", "resource": "StatQuest: Cross Validation, Confusion Matrix, ROC", "task": "Evaluate previous models with proper metrics", "output": "Evaluation report notebook", "hours": 2.5},
            {"day": 12, "objective": "Feature engineering", "resource": "Kaggle Feature Engineering micro-course", "task": "Engineer features for Titanic dataset, improve accuracy", "output": "Improved model with feature engineering", "hours": 3},
            {"day": 13, "objective": "Probability for ML", "resource": "StatQuest: Bayes Theorem, Distributions", "task": "Implement Naive Bayes from scratch", "output": "Custom NB implementation + comparison with sklearn", "hours": 3},
            {"day": 14, "objective": "Week 2 review + Kaggle submission", "resource": "Kaggle Titanic competition", "task": "Submit best Titanic model to Kaggle", "output": "Kaggle submission + score screenshot", "hours": 4},
            {"day": 15, "objective": "Neural networks: Concepts", "resource": "3Blue1Brown Neural Networks series (Ep 1-2)", "task": "Implement a perceptron from scratch in NumPy", "output": "Working perceptron code", "hours": 3},
            {"day": 16, "objective": "Intro to PyTorch", "resource": "PyTorch official: 60-minute blitz", "task": "Build and train a simple neural net in PyTorch", "output": "PyTorch training script", "hours": 3.5},
            {"day": 17, "objective": "PyTorch: CNNs", "resource": "PyTorch CNN tutorial", "task": "Train a CNN on MNIST/Fashion-MNIST", "output": "CNN achieving >95% accuracy", "hours": 3},
            {"day": 18, "objective": "Calculus for backpropagation", "resource": "3Blue1Brown: Backpropagation calculus", "task": "Manually compute gradients for a small network", "output": "Gradient computation notebook", "hours": 2.5},
            {"day": 19, "objective": "Transfer learning", "resource": "PyTorch transfer learning tutorial", "task": "Fine-tune a pretrained model on custom image dataset", "output": "Transfer learning notebook", "hours": 3},
            {"day": 20, "objective": "Flagship project: Start", "resource": "Project planning + dataset collection", "task": "Define problem, collect data, set up project repo", "output": "GitHub repo with README and data folder", "hours": 3},
            {"day": 21, "objective": "Week 3 review + flagship project EDA", "resource": "Your collected dataset", "task": "Complete EDA and preprocessing for flagship project", "output": "EDA notebook in project repo", "hours": 4},
            {"day": 22, "objective": "Flagship project: baseline model", "resource": "Scikit-learn + PyTorch", "task": "Train baseline model, establish benchmark metrics", "output": "Baseline model with evaluation", "hours": 3.5},
            {"day": 23, "objective": "Flagship project: improved model", "resource": "Hyperparameter tuning guides", "task": "Improve model with feature engineering + tuning", "output": "Improved model beating baseline", "hours": 3.5},
            {"day": 24, "objective": "Model deployment: Flask/FastAPI", "resource": "FastAPI ML serving tutorial", "task": "Wrap your model in a REST API", "output": "Runnable API endpoint", "hours": 3},
            {"day": 25, "objective": "Docker basics for ML", "resource": "Docker official getting started", "task": "Containerize your ML API", "output": "Dockerfile + docker-compose.yml", "hours": 3},
            {"day": 26, "objective": "Flagship project: Frontend", "resource": "Streamlit or Gradio tutorial", "task": "Build a simple UI for your ML model", "output": "Interactive demo app", "hours": 3},
            {"day": 27, "objective": "Experiment tracking with MLflow", "resource": "MLflow quickstart guide", "task": "Log experiments for your flagship project", "output": "MLflow dashboard with tracked runs", "hours": 2.5},
            {"day": 28, "objective": "Week 4 review + flagship project polish", "resource": "Code review best practices", "task": "Clean code, add docstrings, write tests", "output": "Production-quality codebase", "hours": 4},
            {"day": 29, "objective": "Portfolio + documentation", "resource": "Technical writing guides", "task": "Write detailed README, add architecture diagram", "output": "Portfolio-ready project documentation", "hours": 3},
            {"day": 30, "objective": "Final review + LinkedIn update", "resource": "LinkedIn optimization guide", "task": "Update LinkedIn with new skills, publish project post", "output": "Updated profile + project showcase post", "hours": 2.5},
        ],
        "weekly_milestones": [
            {"week": 1, "milestone": "Data science foundations: NumPy, Pandas, visualization, and linear algebra. Completed Titanic EDA.", "skills_gained": ["NumPy", "Pandas", "Matplotlib", "Linear Algebra basics", "EDA"]},
            {"week": 2, "milestone": "Classical ML mastery: Built classifiers, regressors, and submitted to Kaggle.", "skills_gained": ["Scikit-learn", "Supervised learning", "Model evaluation", "Feature engineering", "Probability"]},
            {"week": 3, "milestone": "Deep learning fundamentals: Built neural networks in PyTorch, started flagship project.", "skills_gained": ["PyTorch", "CNNs", "Transfer learning", "Backpropagation", "Neural network architecture"]},
            {"week": 4, "milestone": "Production ML: Deployed model as API, containerized, tracked experiments. Portfolio-ready project complete.", "skills_gained": ["Model deployment", "Docker", "MLflow", "FastAPI", "Technical writing"]},
        ],
    },
    "flagship_project": {
        "title": "MedScan: AI-Powered Medical Image Classifier",
        "problem_statement": "Build an end-to-end ML system that classifies medical images (e.g., chest X-rays) to detect pneumonia, providing a web interface for healthcare workers in low-resource settings.",
        "tech_stack": ["Python", "PyTorch", "FastAPI", "Streamlit", "Docker", "MLflow"],
        "weekly_features": [
            {"week": 1, "feature": "Data pipeline", "description": "Download and preprocess the ChestX-ray14 dataset. Build data loaders, augmentation pipeline, and train/val/test splits."},
            {"week": 2, "feature": "Baseline classifier", "description": "Train a baseline CNN and a fine-tuned ResNet-18. Compare performance with proper metrics (AUC, sensitivity, specificity)."},
            {"week": 3, "feature": "Model optimization", "description": "Hyperparameter tuning, learning rate scheduling, and ensemble methods. Add Grad-CAM visualizations for explainability."},
            {"week": 4, "feature": "Deployment & demo", "description": "REST API with FastAPI, Streamlit frontend for image upload + prediction, Dockerized for easy deployment. Full documentation."},
        ],
        "portfolio_quality": "This project demonstrates end-to-end ML skills: data engineering, model development, explainability (Grad-CAM), deployment, and containerization. It addresses a real healthcare problem, making it compelling for interviews and resume.",
    },
    "reasoning": "The student has solid Python basics and good collaboration skills, but lacks the core ML stack entirely. The 30-day plan prioritizes math foundations and hands-on framework experience in weeks 1-2, progresses to deep learning in week 3, and culminates in a deployment-ready portfolio project in week 4. This path addresses all critical gaps while building on existing Python strength.",
}


MOCK_ADAPT_RESPONSE = {
    "adaptation_reasoning": "The student missed 7 days (days 8-14), losing the entire classical ML week. Since deep learning requires understanding of basic ML concepts, we need to compress the essential Scikit-learn content into the first 2 remaining days before proceeding with PyTorch. The flagship project scope is reduced to use a simpler model architecture.",
    "adapted_roadmap": {
        "days": [
            {"day": 15, "objective": "Crash course: Scikit-learn essentials", "resource": "Scikit-learn crash course (Data School YouTube)", "task": "Train classifier + regressor on Iris and Boston datasets", "output": "Two working model notebooks", "hours": 4},
            {"day": 16, "objective": "Model evaluation crash course", "resource": "StatQuest: Cross Validation + Confusion Matrix", "task": "Evaluate models with proper metrics, understand overfitting", "output": "Evaluation notebook with cross-validation", "hours": 3},
            {"day": 17, "objective": "Neural networks: Concepts + PyTorch intro", "resource": "3Blue1Brown NN series + PyTorch 60-min blitz", "task": "Build first neural net in PyTorch", "output": "Working PyTorch training script", "hours": 4},
            {"day": 18, "objective": "PyTorch: CNNs on MNIST", "resource": "PyTorch CNN tutorial", "task": "Train CNN on Fashion-MNIST", "output": "CNN achieving >90% accuracy", "hours": 3},
            {"day": 19, "objective": "Transfer learning (compressed)", "resource": "PyTorch transfer learning tutorial", "task": "Fine-tune ResNet on a small custom dataset", "output": "Transfer learning notebook", "hours": 3},
            {"day": 20, "objective": "Flagship project: Setup + EDA", "resource": "Chest X-ray dataset", "task": "Set up repo, download data, complete EDA", "output": "GitHub repo with EDA notebook", "hours": 4},
            {"day": 21, "objective": "Flagship project: Baseline model", "resource": "PyTorch + transfer learning", "task": "Train baseline model, evaluate", "output": "Baseline with initial metrics", "hours": 4},
            {"day": 22, "objective": "Flagship project: Model improvement", "resource": "Fine-tuning techniques", "task": "Improve model performance, add Grad-CAM", "output": "Improved model + explainability", "hours": 4},
            {"day": 23, "objective": "Flagship project: API deployment", "resource": "FastAPI tutorial", "task": "Build REST API for model predictions", "output": "Working API endpoint", "hours": 3},
            {"day": 24, "objective": "Flagship project: Simple frontend", "resource": "Streamlit crash course", "task": "Build image upload + prediction UI", "output": "Working Streamlit app", "hours": 3},
            {"day": 25, "objective": "Docker + documentation", "resource": "Docker basics for Python", "task": "Containerize app, write README", "output": "Dockerized project with docs", "hours": 3},
            {"day": 26, "objective": "Portfolio polish", "resource": "Technical writing guide", "task": "Add architecture diagram, clean code, add tests", "output": "Portfolio-ready codebase", "hours": 3},
            {"day": 27, "objective": "Kaggle quick submission", "resource": "Kaggle getting started competition", "task": "Submit a Kaggle entry using your new skills", "output": "Kaggle submission + score", "hours": 2.5},
            {"day": 28, "objective": "Fill remaining gaps: Statistics review", "resource": "StatQuest playlist (key videos)", "task": "Watch and summarize 5 key statistics concepts", "output": "Study notes", "hours": 2},
            {"day": 29, "objective": "LinkedIn + GitHub profile update", "resource": "LinkedIn optimization tips", "task": "Update profiles, publish project showcase", "output": "Updated online presence", "hours": 2},
            {"day": 30, "objective": "Final review and next steps planning", "resource": "Self-assessment", "task": "Review all projects, identify areas for continued learning", "output": "Personal learning roadmap for month 2", "hours": 2},
        ],
        "weekly_milestones": [
            {"week": 3, "milestone": "Recovered ML fundamentals + started deep learning with PyTorch. Compressed weeks 2-3 essentials.", "skills_gained": ["Scikit-learn basics", "Model evaluation", "PyTorch", "CNNs", "Transfer learning"]},
            {"week": 4, "milestone": "Completed flagship project with deployment. Scope reduced but still portfolio-worthy.", "skills_gained": ["FastAPI", "Streamlit", "Docker", "End-to-end ML project", "Portfolio development"]},
        ],
    },
    "adapted_project": {
        "changes": "Reduced from 4-week progressive build to 2-week intensive build. Dropped ensemble methods and advanced hyperparameter tuning. Kept core value: deployed ML model with explainability.",
        "weekly_features": [
            {"week": 3, "feature": "Data + Model", "description": "Combined EDA, baseline, and improvement into one intensive week. Focus on transfer learning rather than training from scratch."},
            {"week": 4, "feature": "Deploy + Polish", "description": "API, frontend, Docker, and documentation. Simplified UI but still production-quality."},
        ],
    },
    "motivation": "Missing a week feels like a setback, but you've already built strong Python and data foundations. The adapted plan compresses the essentials without cutting corners on what matters most — by day 30, you'll still have a deployed ML project on your resume. Let's go! 🚀",
}
