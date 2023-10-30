from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from pydantic import BaseModel, Field
from langchain_experimental.generative_agents import (
    GenerativeAgent,
    GenerativeAgentMemory,
)
from companion_agent.memory import AgentMemory
from companion_agent.utils.chUtil import check_path

FILE_PATH = os.path.abspath(__file__)
ROOT_PATH, FILE_NAME = os.path.split(FILE_PATH)

logger = logging.getLogger(__name__)

class CompanionAgent():
    """An Agent as a character with memory and innate characteristics."""

    

    def __init__(
            self,
            save_path: str,
            name: str,
            status: str,
            memory: AgentMemory,
            llm: BaseLanguageModel,
            age: Optional[int] = None,
            traits: str = "N/A",
            characters: Dict[str, dict] = {},
            verbose: bool = False,
            summary: str = "",  #: :meta private:
            summary_refresh_seconds: int = 3600,
            last_refreshed: datetime = datetime.now(),
            daily_summaries: List[str] = [],
    ):
        kwargs = {
            'name': name, 'status': status, 'memory': memory, 
            'llm': llm, 'age': age, 'traits': traits, 'characters': characters, 
            'verbose': verbose, 'summary': summary, 'summary_refresh_seconds': summary_refresh_seconds, 
            'last_refreshed': last_refreshed, 'daily_summaries': daily_summaries, 'save_path': save_path
        }
        self.__dict__.update(kwargs)
        check_path(self.save_path)
        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename=os.path.join(self.save_path,'run_agent.log'),
                    filemode='a')

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    # LLM-related methods
    @staticmethod
    def _parse_list(text: str) -> List[str]:
        """Parse a newline-separated string into a list of strings."""
        lines = re.split(r"\n", text.strip())
        return [re.sub(r"^\s*\d+\.\s*", "", line).strip() for line in lines]

    def chain(self, prompt: PromptTemplate) -> LLMChain:
        return LLMChain(
            llm=self.llm, prompt=prompt, verbose=self.verbose, memory=self.memory
        )

    def _get_entity_from_observation(self, observation: str) -> str:
        if self.memory.language == 'en':
            prompt = PromptTemplate.from_template(
                "What is the observed entity in the following observation? {observation}"
                + "\nEntity="
            )
        else:
            prompt = PromptTemplate.from_template(
                "{observation} 中观察到的实体是谁？"
                + "\n实体="
            )
        return self.chain(prompt).run(observation=observation).strip()

    def _get_entity_action(self, observation: str, entity_name: str) -> str:
        if self.memory.language == 'en':
            prompt = PromptTemplate.from_template(
                "What is the {entity} doing in the following observation? {observation}"
                + "\nThe {entity} is"
            )
        else:
            prompt = PromptTemplate.from_template(
                "观察:{observation}\n"
                +"通过观察到的内容，请回答{entity}在做什么"
                + "\n{entity}在"
            )
        return (
            self.chain(prompt).run(entity=entity_name, observation=observation).strip()
        )

    def summarize_related_memories(self, observation: str, role: str = None, now: Optional[datetime] = None, intent_recognition = True) -> str:
        """Summarize memories that are most relevant to an observation."""
        
        if not role: 
            entity_name = self._get_entity_from_observation(observation)
        else:
            entity_name = role
        # entity_action = self._get_entity_action(observation, entity_name)
        if self.memory.language == 'en':
            prompt = PromptTemplate.from_template(
                """
                {q1}?
                Context from memory:
                {relevant_memories}
                Relevant context: 
                """
            )
            q1 = f"What is the relationship between {self.name} and {entity_name}"
            # q2 = f"{entity_name} is {entity_action}"
        else:
            prompt = PromptTemplate.from_template(
                """
                相关记忆：
                {relevant_memories}
                当前发生的事：
                {most_recent_memories}
                {q1}？
                """
            )
            Q1 = f"""请推断并简述 {self.name} 和 {entity_name} 的关系。\n
                    仅回答关系 \n
                    {self.name} 和 {entity_name}的关系：\n """
            # q1 = f"{entity_name} 和 {self.name} 是什么关系"
            # q1 = f"{self.name} 和 {entity_name}"
            q1 = f"{entity_name} 是谁"
            Q2 = f"请简要概括 {entity_name} 的人物特点和立场，不要美化修饰"
            q2 = f"{entity_name} 是谁"
            Q3 = f"{self.name}觉得为什么{entity_name}会{observation}"
            q3 = f"{entity_name}{observation}"
            Q4 = f"简要概括相关记忆"
            q4 = f"{entity_name}{observation}"
        
        start = datetime.now()

        current_time = datetime.now() if now is None else now
        if entity_name in self.characters:
            obj = self.characters[entity_name]
        else:
            self.characters[entity_name]={'last_refreshed':datetime.now(), 'force_refresh': False, 'description': None, 'relationship': None}
            obj = self.characters[entity_name]
        ## 创建线程池
        tpe = ThreadPoolExecutor(4)
        task_list = []
        results = {}
        chain = self.chain(prompt=prompt)

        def band(key, **kwargs):
            return (key, chain.run(**kwargs).strip())

        since_refresh = (current_time - obj['last_refreshed']).seconds
        if (
            since_refresh >= self.summary_refresh_seconds
            or not obj['description']
            or not obj['relationship']
            or obj['force_refresh']
        ):
            obj['last_refreshed'] = current_time
            task_list += [tpe.submit(band, key='relationship', q1=Q1, queries=[q1], most_recent_memories='', depth=0, importance_weight=0.0, threshold=0.8, top_k=10)]
            task_list += [tpe.submit(band, key='description', q1=Q2, queries=[q2], most_recent_memories='', depth=0, importance_weight=0.5, threshold=0.7, top_k=10)]
            # obj['relationship'] = chain.run(q1=Q1, queries=[q1], most_recent_memories='', depth=0, importance_weight=0.0, threshold=0.8, top_k=10).strip()
            # obj['description'] = chain.run(q1=Q2, queries=[q2], most_recent_memories='', depth=0, importance_weight=0.5, threshold=0.7, top_k=10).strip()
        if intent_recognition: task_list += [tpe.submit(band, key='intent', q1=Q3, queries=[q3], depth=1, most_recent_memories='', importance_weight=0.0, threshold=0.7, top_k=20)]
        task_list += [tpe.submit(band, key='related', q1=Q4, queries=[q4], depth=1, most_recent_memories='', importance_weight=0.0, threshold=0.8, top_k=10, time_sorted = True)]
        # results += [self.chain(prompt=prompt).run(q1=Q3, queries=[q3], most_recent_memories='', depth=1, importance_weight=0.0, threshold=0.7, top_k=20).strip()]
        
        for future in as_completed(task_list):
            result = future.result()
            results[result[0]] = result[1]
        if 'relationship' in results: obj['relationship'] = results['relationship']
        else: results['relationship'] = obj['relationship']
        if 'description' in results: obj['description'] = results['description']
        else: results['description'] = obj['description']
        if not 'intent' in results: results['intent'] = ''
        results = [results['relationship'], results['description'], results['intent'], results['related']]

        end = datetime.now()
        relationship = ' '.join(results[0].split('\n'))
        logger.info(f"Reaction: relationship = {relationship}")
        description = ' '.join(results[1].split('\n'))
        logger.info(f"Reaction: description = {description}")
        intent = ' '.join(results[2].split('\n'))
        logger.info(f"Reaction: intent = {intent}")
        related = ' '.join(results[3].split('\n'))
        logger.info(f"Reaction: related = {related}")
        logger.info(f"Reaction: summarize_related_memories in {end-start}s")

        return '\n'.join(results)
    
    def stylize(self, role:tuple, user:tuple,question,reference):
        from langchain.prompts import (
            ChatPromptTemplate,
            SystemMessagePromptTemplate,
            HumanMessagePromptTemplate,
        )
        from langchain.chat_models import ChatOpenAI
        def question_stylize(role,question):
            system_message_prompt = SystemMessagePromptTemplate.from_template("你是一个说话风格迁移模型。")
            with open(os.path.join(ROOT_PATH, "template/question_stylize_template.txt"), "r", encoding = 'utf-8') as f:
                human_template = f.read()
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
            inputs = {"role": role[0],"role_description":role[1],"question":question}
            prompt = chat_prompt.format_prompt(**inputs).to_messages()
            # chat = ChatGLM()
            chat = ChatOpenAI(model="gpt-4")
            result = chat(prompt).content
            return result
        
        stylize_question=question_stylize(role,question)
        print(stylize_question)
        # system_message_prompt = SystemMessagePromptTemplate.from_template("你是一个问答模型。")
        with open(os.path.join(ROOT_PATH, "template/answer_stylize_template.txt"), "r", encoding = 'utf-8') as f:
            human_template = f.read()
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
        inputs = {"role": role[0],"role_description":role[1],
                "user":user[0],"user_description":user[1],
                "question":stylize_question,"reference":reference}
        prompt = chat_prompt.format_prompt(**inputs).to_messages()
        # chat = ChatGLM()
        chat = ChatOpenAI(model="gpt-4")
        result = chat(prompt).content
        return result

    def _generate_reaction(
        self, observation: str, suffix: str, now: Optional[datetime] = None, role: str = None, addition: dict = None, intent_recognition = None
    ) -> str:
        """React to a given observation or dialogue act."""
        if not addition: addition = {}
        addition_str = "\n".join([f"{key}: {value}" for key,value in addition.items()])
        if self.memory.language == 'en':
            prompt = PromptTemplate.from_template(
                "{agent_summary_description}"
                + "\nIt is {current_time}."
                + "\n{agent_name}'s status: {agent_status}"
                + "\n{addition_str}"
                + "\nSummary of relevant context from {agent_name}'s memory:"
                + "\n{relevant_memories}"
                + "\nMost recent observations: {most_recent_memories}"
                + "\nObservation: {observation}"
                + "\n\n"
                + suffix
            )
        else:
            prompt = PromptTemplate.from_template(
                "{agent_summary_description}"
                + "\n现在是 {current_time}."
                + "\n{agent_name} 的当前状态是：{agent_status}"
                + "\n{agent_name} 的相关记忆概括如下："
                + "\n{relevant_memories}"
                + "{addition_str}"
                + "\n正在发生的事：{most_recent_memories}"
                + "\n观察到：{observation}"
                + "\n\n"
                + suffix
            )

        start = datetime.now()

        tpe = ThreadPoolExecutor(2)
        task_list = []
        def band(key, func, *args, **kwargs):
            return (key, func(*args, **kwargs).strip())
        task_list += [tpe.submit(band, 'agent_summary_description', self.get_summary, now=now)]
        task_list += [tpe.submit(band, 'relevant_memories_str', self.summarize_related_memories, observation, role, intent_recognition=intent_recognition)]
        for future in as_completed(task_list):
            result = future.result()
            if 'agent_summary_description' == result[0]: agent_summary_description = result[1]
            else: relevant_memories_str = result[1]
        # agent_summary_description = self.get_summary(now=now)
        # relevant_memories_str = self.summarize_related_memories(observation, role, intent_recognition=intent_recognition)
        
        current_time_str = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if now is None
            else now.strftime("%Y-%m-%d %H:%M:%S")
        )
        kwargs: Dict[str, Any] = dict(
            agent_summary_description=agent_summary_description,
            current_time=current_time_str,
            relevant_memories=relevant_memories_str,
            agent_name=self.name,
            addition_str= '\n'+addition_str if addition_str else '',
            observation=role+observation if role else observation,
            agent_status=self.status,
        )
        # consumed_tokens = self.llm.get_num_tokens(
        #     prompt.format( **kwargs)
        # )
        kwargs[self.memory.most_recent_memories_token_key] = 3

        cropus = datetime.now()
        logger.info(f"Reaction: {str(kwargs)}")
        logger.info(f"Reaction: prepare cropus in {(cropus-start).seconds}s")
        
        reaction = self.chain(prompt=prompt).run(**kwargs).strip()
        
        end = datetime.now()
        logger.info(f"Reaction: generate in {(end-cropus).seconds}s")

        return reaction

    def _clean_response(self, text: str) -> str:
        return re.sub(f"^{self.name} ", "", text.strip()).strip()
    
    def save_context_controller(self, save = True, kwargs = {}):
        if save:
            self.memory.save_context(
                {}, kwargs,
            )

    def generate_reaction(
        self, observation: str, role: str = '', now: Optional[datetime] = None, addition: dict = None, log_time = False, intent_recognition = True, stylize = False, save_reaction = True, fast_mode = False
    ) -> Tuple[bool, str]:
        # fast_mode 开启时单论对话为一个事件
        logger.info("Generate Reaction: ############################# start ##################################")
        kwargs = {'role':role, 'observation':observation, 'now':now, 'addition':addition, 
                  'log_time':log_time, 'intent_recognition':intent_recognition, 'stylize':stylize,
                  'save_reaction':save_reaction, 'fast_mode':fast_mode}
        logger.info(f"Generate Reaction: {str(kwargs)}")
        """React to a given observation."""
        if self.memory.language == 'en':
            call_to_action_template = (
                "Should {agent_name} react to the observation, and if so,"
                + " what would be an appropriate reaction? Respond in one line."
                + ' If the action is to engage in dialogue, write:\nSAY: "what to say"'
                + "\notherwise, write:\nREACT: {agent_name}'s reaction (if anything)."
                + "\nEither do nothing, react, or say something but not both.\n\n"
            )
            actstr = 'say: '
        else:
            call_to_action_template = (
                "针对观察到的事 {agent_name} 会做什么？"
                + '请在单行内给出合理的响应行为。回答不要啰嗦，也不要太过于正式或礼貌。'
                + '如果响应行为是“做”，请回答：\nREACT: "要做的事"'
                + '如果响应行为是“说”，请回答：\nSAY: "要说的话"'
                + '否则，请回答：\nNOTHING'
                + "\n要么说些什么，要么做些什么，要么什么都不做，三选一。\n\n"
            )
            actstr = '说：'
        
        start = datetime.now()
        

        self.save_context_controller(
            save_reaction,
            {
                self.memory.add_memory_key: f"{observation}",
                'role': role,
                'host': False,
                self.memory.now_key: now,
                'seg': True if fast_mode else None
            },
        )

        saved1 = datetime.now()
        logger.info(f"Generate Reaction: saved observation in {(saved1-start).seconds}s")

        full_result = self._generate_reaction(
            f"{observation}", call_to_action_template, now=now, role=role, addition=addition, intent_recognition = intent_recognition
        )
        result = full_result.strip().split("\n")[0]

        generated = datetime.now()
        logger.info(f"Generate Reaction: generate {result}")
        logger.info(f"Generate Reaction: generated reaction in {(generated-saved1).seconds}s")

        do_something = False
        if "REACT:" in result:
            do_something = True
            reaction = self._clean_response(result.split("REACT:")[-1])
            result = reaction
            self.save_context_controller(
                save_reaction,
                {
                    self.memory.add_memory_key: reaction,
                    'role': self.name,
                    'host': True,
                    self.memory.now_key: now,
                    'seg': False
                },
            )
            
        elif "SAY:" in result:
            do_something = True
            said_value = self._clean_response(result.split("SAY:")[-1])
            result = f"{actstr}{said_value}"
            self.save_context_controller(
                save_reaction,
                {
                    self.memory.add_memory_key: f"{actstr}{said_value}",
                    'role': self.name,
                    'host': True,
                    self.memory.now_key: now,
                    'seg': False
                },
            )

        end = datetime.now()
        logger.info(f"Generate Reaction: react by {result}")
        logger.info(f"Generate Reaction: saved reaction in {(end-generated).seconds}s")
        logger.info(f"Generate Reaction: finish in {(end-start).seconds}s")
        return do_something, result

    def generate_dialogue_response(
        self, observation: str, role: str = '', now: Optional[datetime] = None, addition: dict = None, log_time = False, intent_recognition = True, stylize = False, save_response = True, fast_mode = False
    ) -> Tuple[bool, str]:
        """React to a given observation."""
        logger.info("Generate Reaction: ############################# start ##################################")
        kwargs = {'role':role, 'observation':observation, 'now':now, 'addition':addition,
                  'log_time':log_time, 'intent_recognition':intent_recognition, 'stylize':stylize,
                  'save_response':save_response, 'fast_mode':fast_mode}
        logger.info(f"Generate Dialogue Response: {str(kwargs)}")
        if self.memory.language == 'en':
            call_to_action_template = (
                "What would {agent_name} say? To end the conversation, write:"
                ' GOODBYE: "what to say". Otherwise to continue the conversation,'
                ' write: SAY: "what to say next"\n\n'
            )
            actstr = 'say: '
            observation = f"say: \"{observation}\""

        else:
            call_to_action_template = (
                "针对观察到的事 {agent_name} 会说什么？"
                '回答不要啰嗦，也不要太过于正式或礼貌。'
                '如果要结束对话回答： GOODBYE: "要说的话". '
                '其他情况请回答： SAY: "要说的话"\n\n'
            )
            actstr = '说：'
            observation = f"说：“{observation}”"
        
        start = datetime.now()

        self.save_context_controller(
            save_response,
            {
                self.memory.add_memory_key: f"{observation}",
                'role': role,
                'host': False,
                self.memory.now_key: now,
                'seg': True if fast_mode else None
            },
        )

        saved1 = datetime.now()
        logger.info(f"Generate Dialogue Response: saved observation in {(saved1-start).seconds}s")

        full_result = self._generate_reaction(
            f"{observation}", call_to_action_template, now=now, role=role, addition=addition, intent_recognition = intent_recognition
        )
        result = full_result.strip().split("\n")[0]

        generated = datetime.now()
        logger.info(f"Generate Dialogue Response: generate {result}")
        logger.info(f"Generate Dialogue Response: generated response in {(generated-saved1).seconds}s")

        do_something = False
        if "GOODBYE:" in result:
            do_something = True
            farewell = self._clean_response(result.split("GOODBYE:")[-1])
            result = f"{farewell}"
            self.save_context_controller(
                save_response,
                {
                    self.memory.add_memory_key: f"{actstr}{farewell}",
                    'role': self.name,
                    'host': True,
                    self.memory.now_key: now,
                    'seg': False
                },
            )
        elif "SAY:" in result:
            do_something = True
            response_text = self._clean_response(result.split("SAY:")[-1])
            result = f"{response_text}"
            self.save_context_controller(
                save_response,
                {
                    self.memory.add_memory_key: f"{actstr}{response_text}",
                    'role': self.name,
                    'host': True,
                    self.memory.now_key: now,
                    'seg': False
                },
            )
            
        end = datetime.now()
        logger.info(f"Generate Dialogue Response: respond by {result}")
        logger.info(f"Generate Dialogue Response: saved response in {(end-generated).seconds}s")
        logger.info(f"Generate Dialogue Response: finish in {(end-start).seconds}s")
        return do_something, result

    ######################################################
    # Agent stateful' summary methods.                   #
    # Each dialog or response prompt includes a header   #
    # summarizing the agent's self-description. This is  #
    # updated periodically through probing its memories  #
    ######################################################
    def _compute_agent_summary(self) -> str:
        """"""
        if self.memory.language == 'en': 
            prompt = PromptTemplate.from_template(
                "How would you summarize {name}'s core characteristics given the"
                + " following statements:\n"
                + "{relevant_memories}"
                + "Do not embellish."
                + "\n\nSummary: "
            )
            queries=[f"{self.name}'s core characteristics"]
        else:
            prompt = PromptTemplate.from_template(
                "相关信息:\n"
                + "{relevant_memories}\n"
                + "通过上述信息，你怎么概括{name}的关键性格特征\n"
                + "不要美化修饰"
                + "\n\n概括: "
            )
            queries=[f"{self.name}是谁"]

        # The agent seeks to think about their core characteristics.
        return (
            self.chain(prompt)
            .run(name=self.name, queries=queries, depth=0, importance_weight=0.3, threshold=0.7)
            .strip()
        )

    def get_summary(
        self, force_refresh: bool = False, now: Optional[datetime] = None
    ) -> str:
        """Return a descriptive summary of the agent."""
        start = datetime.now()
        current_time = datetime.now() if now is None else now
        since_refresh = (current_time - self.last_refreshed).seconds
        if (
            not self.summary
            or since_refresh >= self.summary_refresh_seconds
            or force_refresh
        ):
            self.summary = self._compute_agent_summary()
            self.last_refreshed = current_time
        age = self.age if self.age is not None else "N/A"
        
        if self.memory.language == 'en':
            result =  (
                f"Name: {self.name} (age: {age})"
                + f"\nInnate traits: {self.traits}"
                + f"\n{self.summary}"
            )
        else:
            result = (
                f"姓名：{self.name} (年龄：{age})"
                + f"\n特征：{self.traits}"
                + f"\n{self.summary}"
            )

        end = datetime.now()
        agent_summary_description = ' '.join(result.split('\n'))
        logger.info(f"Reaction: agent_summary_description = {agent_summary_description}")
        logger.info(f"Reaction: get_summary in {end-start}s")
        return result

    def get_full_header(
        self, force_refresh: bool = False, now: Optional[datetime] = None
    ) -> str:
        """Return a full header of the agent's status, summary, and current time."""
        now = datetime.now() if now is None else now
        summary = self.get_summary(force_refresh=force_refresh, now=now)
        current_time_str = now.strftime("%B %d, %Y, %I:%M %p")
        return (
            f"{summary}\nIt is {current_time_str}.\n{self.name}'s status: {self.status}"
        )
