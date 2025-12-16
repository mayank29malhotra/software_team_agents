from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class EngineeringTeam():
    """
    EngineeringTeam crew - A complete software engineering team with 7 specialized AI agents.
    
    Workflow (Sequential):
    1. Requirements Analyst → Validates & structures requirements
    2. Engineering Lead → Creates technical design
    3. Backend Engineer → Implements backend code
    4. Frontend Engineer → Creates Gradio demo UI
    5. Code Reviewer → Reviews code for security, quality, performance
    6. Test Engineer → Writes tests informed by code review
    7. Doc Writer → Generates documentation
    
    Memory is enabled for:
    - Cross-task context sharing within a run
    - Learning patterns across multiple runs (long-term memory)
    - Entity tracking for consistency
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ==================== AGENTS ====================
    
    @agent
    def requirements_analyst(self) -> Agent:
        """Business Analyst who validates requirements before design starts"""
        return Agent(
            config=self.agents_config['requirements_analyst'],
            verbose=True,
        )

    @agent
    def engineering_lead(self) -> Agent:
        """Engineering Lead who creates detailed technical designs"""
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        """Python Engineer who implements the technical design"""
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        """Gradio expert who creates simple demo UIs"""
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def code_reviewer(self) -> Agent:
        """Senior Code Reviewer who ensures quality before testing"""
        return Agent(
            config=self.agents_config['code_reviewer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        """QA Engineer who writes comprehensive unit tests"""
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def doc_writer(self) -> Agent:
        """Technical Documentation Engineer who generates README, API docs, and quickstart guides"""
        return Agent(
            config=self.agents_config['doc_writer'],
            verbose=True,
        )

    # ==================== TASKS ====================

    @task
    def requirements_analysis_task(self) -> Task:
        """Validates requirements, detects contradictions, edge cases, and complexity risks"""
        return Task(
            config=self.tasks_config['requirements_analysis_task']
        )

    @task
    def design_task(self) -> Task:
        """Creates detailed technical design based on validated requirements"""
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        """Implements the backend code based on design"""
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        """Creates Gradio UI to demonstrate the backend"""
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def code_review_task(self) -> Task:
        """Reviews code for security, quality, performance, and requirements compliance"""
        return Task(
            config=self.tasks_config['code_review_task'],
        )

    @task
    def test_task(self) -> Task:
        """Writes comprehensive unit tests informed by code review findings"""
        return Task(
            config=self.tasks_config['test_task'],
        )

    @task
    def documentation_task(self) -> Task:
        """Generates README, API docs, and quickstart examples"""
        return Task(
            config=self.tasks_config['documentation_task'],
        )   

    @crew
    def crew(self) -> Crew:
        """
        Creates the Engineering Team crew with 7 specialized agents.
        
        Memory Configuration:
        - memory=True: Enables all memory types (short-term, long-term, entity)
        - Short-term: Agents share context within the current run
        - Long-term: Crew learns patterns across multiple runs
        - Entity: Tracks modules, classes, and requirements for consistency
        
        This means:
        1. Code Reviewer knows what Requirements Analyst flagged as risks
        2. Test Engineer sees Code Review findings to prioritize tests
        3. On subsequent runs, agents remember successful patterns
        """
        return Crew(
            agents=self.agents,  # Automatically includes all @agent decorated methods
            tasks=self.tasks,    # Automatically includes all @task decorated methods
            process=Process.sequential,
            verbose=True,
            # Memory enables learning and context sharing
            memory=True,
            # Respect context window limits for better memory retrieval
            respect_context_window=True,
        )