import streamlit as st

st.set_page_config(page_title="MECE Builder", layout="wide", page_icon="📊")
st.title("MECE Builder")

HTML_PAGE_TEXT = """
    <h1>O que é um MECE</h1>
    <p>Um MECE (Mutuamente Exclusivo e Coletivamente Exaustivo) é um princípio fundamental em análise e resolução de problemas que visa organizar informações de forma clara, completa e sem sobreposições. Aqui estão as principais características e exemplos de uso desse princípio:</p>
    
    <h2>Características Gerais do MECE</h2>
    <ol>
        <li><strong>Mutuamente Exclusivo (ME)</strong>: As categorias ou opções não se sobrepõem; cada item pertence a uma única categoria.</li>
        <li><strong>Coletivamente Exaustivo (CE)</strong>: As categorias ou opções cobrem todas as possibilidades, garantindo que todas as partes do problema ou da situação sejam consideradas.</li>
    </ol>
    
    <h2>Exemplos de Uso</h2>
    <h3>Análise de Mercado</h3>
    <ul>
        <li><strong>Mutuamente Exclusivo</strong>: Dividir o mercado em segmentos distintos, como geográficos (Norte, Sul, Leste, Oeste) ou demográficos (jovens, adultos, idosos), onde cada cliente pertence a apenas um segmento.</li>
        <li><strong>Coletivamente Exaustivo</strong>: Garantir que todos os clientes potenciais sejam incluídos em um dos segmentos, sem deixar nenhum grupo de fora.</li>
    </ul>
    
    <h3>Desenvolvimento de Produtos</h3>
    <ul>
        <li><strong>Mutuamente Exclusivo</strong>: Categorizar funcionalidades de um produto em áreas como design, funcionalidade, e preço, onde cada aspecto é avaliado separadamente.</li>
        <li><strong>Coletivamente Exaustivo</strong>: Cobrir todas as características importantes do produto, desde a estética até a usabilidade e o custo, para garantir que nenhuma área crucial seja negligenciada.</li>
    </ul>
    
    <h3>Planejamento Financeiro</h3>
    <ul>
        <li><strong>Mutuamente Exclusivo</strong>: Dividir despesas em categorias como alimentação, moradia, transporte e lazer, assegurando que cada despesa seja classificada em apenas uma categoria.</li>
        <li><strong>Coletivamente Exaustivo</strong>: Incluir todas as despesas possíveis nas categorias, para ter uma visão completa do orçamento.</li>
    </ul>
    
    <h2>Benefícios do Uso de MECE</h2>
    <ul>
        <li><strong>Clareza</strong>: Facilita a compreensão e análise, evitando ambiguidades e confusões.</li>
        <li><strong>Completude</strong>: Garante que todas as possibilidades são consideradas, reduzindo a chance de omissões.</li>
        <li><strong>Eficiência na Tomada de Decisões</strong>: Ajuda a identificar e focar nos aspectos mais relevantes do problema, melhorando a qualidade das decisões.</li>
    </ul>
    
    <h2>Exemplos Práticos</h2>
    <ul>
        <li><strong>Diagnóstico Empresarial</strong>: Ao analisar a performance de uma empresa, pode-se usar o princípio MECE para categorizar áreas como vendas, operações, marketing e finanças, garantindo que todas as áreas são analisadas de forma completa e sem sobreposição.</li>
        <li><strong>Estratégias de Marketing</strong>: Ao definir o público-alvo, pode-se segmentar o mercado de forma que cada segmento seja único (mutuamente exclusivo) e, juntos, cubram todo o mercado potencial (coletivamente exaustivo).</li>
    </ul>
    
    <p>Em resumo, o princípio MECE é uma ferramenta poderosa para estruturar e analisar problemas de forma sistemática e abrangente, sendo amplamente utilizado em diversas áreas para melhorar a clareza e a eficácia das decisões.</p>
"""

st.write(HTML_PAGE_TEXT, unsafe_allow_html=True)
