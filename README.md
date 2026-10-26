# Documentação de Refatoração - GerenciadorPedidos

Este documento detalha os *code smells* identificados no código original da classe `GerenciadorPedidos` e propõe a estrutura ideal para a sua refatoração aplicando boas práticas de desenvolvimento de software e princípios SOLID.
---
## 📋 Sumário
1. [Resumo dos Code Smells Identificados](#1-resumo-dos-code-smells-identificados)
2. Estratégia de Testes de Caracterização - Estará no arquivo atualizado 
3. [Plano de Refatoração em Passos (Alinhado ao SOLID)](#3-plano-de-refatoração-em-passos-alinhado-ao-solid)
4. [Estrutura de Classes Proposta](#4-estrutura-de-classes-proposta)

---
## 1. Resumo dos Code Smells Identificados

| Code Smell | Descrição no Código Original | Impacto |
| :--- | :--- | :--- |
| **God Class (Classe Deus)** | `GerenciadorPedidos` acumula regras de negócio, persistência CSV, controle de estoque e notificações. | Baixa coesão, alta complexidade ciclomática e dificuldade de manutenção. |
| **Long Method (Método Longo)** | O método `processar_pedido` executa validações, cálculos, persistência e E/S em um único bloco extenso. | Difícil leitura, teste e depuração. |
| **Duplicate Code (Código Duplicado)** | A lógica de descontos e cálculo de frete repete-se quase idêntica em `processar_pedido` e `calcular_orcamento`. | Risco de bugs por divergência de regras ao alterar o código. |
| **Data Clumps (Aglomerados de Dados)** | `processar_pedido` recebe 10 parâmetros soltos na assinatura. | Assinaturas poluídas e forte rigidez na alteração de atributos. |
| **Primitive Obsession (Obsessão por Primitivos)** | Itens do pedido armazenados como listas de strings (`[produto, str(qtd), str(preco)]`), exigindo conversões e índices numéricos mágicos (`item[0]`). | Falta de tipagem estática e segurança de domínio. |
| **Magic Numbers (Números Mágicos)** | Valores como `0.05`, `0.15`, `12.5`, `39.9` e `0.0199` espalhados pelo código sem explicação semântica. | Difícil interpretação e alteração de regras de negócio ou taxas. |

---
## 3. Plano de Refatoração em Passos (Alinhado ao SOLID)
Este documento detalha a execução prática da refatoração da classe `GerenciadorPedidos`, dividida em quatro passos incrementais para garantir que a aplicação permaneça funcional (*testes verdes*) em todas as etapas.

## 📦 Passo 1: Extração de Objetos de Domínio (Value Objects)

Eliminamos a obsessão por primitivos e os aglomerados de dados (*Data Clumps*) encapsulando informações dispersas em classes dedicadas.

### 🎯 Ação
* Criar a classe `ItemPedido` para representar os itens do pedido com tipagem estática (`produto`, `quantidade`, `preco`) em substituição à lista de strings.
* Criar a classe `Endereco` para encapsular os dados de entrega (`rua`, `numero`, `cidade`, `uf`, `cep`).
* Criar a classe `Cliente` para encapsular dados cadastrais e o tipo do cliente (`nome`, `email`, `tipo_cliente`).

### 📐 Princípio SOLID Restaurado
* **SRP (Princípio da Responsabilidade Única):** Cada objeto passa a ser dono de seus próprios atributos e de suas validações intrínsecas (ex: validação de formato de e-mail e de CEP).

## 🧮 Passo 2: Isolação de Regras de Desconto e Frete (Strategy Pattern)

Isolamos a lógica de cálculo complexa que estava duplicada entre os métodos `processar_pedido` e `calcular_orcamento`, substituindo também os números mágicos por constantes nomeadas.

### 🎯 Ação
* Criar a classe `CalculadorDesconto` para centralizar as regras baseadas no tipo de cliente (`COMUM`, `VIP`, `FUNCIONARIO`) e subtotais, utilizando constantes para percentuais e limites (ex: `LIMITE_DESCONTO_MINIMO = 500`).
* Criar a classe `CalculadorFrete` para centralizar as regras por estado (`UF`) e regras de isenção por valor ou status VIP.
* Refatorar `processar_pedido` e `calcular_orcamento` para delegar os cálculos a esses novos componentes.

### 📐 Princípio SOLID Restaurado
* **OCP (Princípio Aberto/Fechado) & SRP:** Novas regras de desconto ou faixas de frete podem ser adicionadas criando novas classes ou estratégias sem modificar o fluxo central de pedidos.

## 🔌 Passo 3: Desacoplamento de Infraestrutura (Repositório e Notificação)

Removemos a responsabilidade de E/S de arquivos e simulação de envio de e-mails de dentro das regras de negócio.

### 🎯 Ação
* Criar a classe `RepositorioPedidoCSV` responsável exclusivamente pela persistência e escrita dos dados no arquivo `pedidos.csv`.
* Criar a classe `ServicoNotificacao` responsável por formatar e simular o envio de e-mails de confirmação e alertas de estoque baixo.

### 📐 Princípio SOLID Restaurado
* **DIP (Princípio da Inversão de Dependência) & SRP:** O domínio de pedidos deixa de conhecer detalhes de sistema de arquivos e canais de comunicação, facilitando mocks em testes unitários.

## 🧩 Passo 4: Redução e Simplificação da Classe Principal

Transformamos a antiga "Classe Deus" em um componente limpo e coeso de orquestração.

### 🎯 Ação
* Reduzir a classe `GerenciadorPedidos` para atuar puramente como um **Orquestrador (Facade)**.
* A classe passa a coordenar a validação de estoque, acionar os calculadores (Passo 2) e delegar a persistência e notificações (Passo 3), mantendo o método principal curto e legível.

### 📐 Princípio SOLID Restaurado
* **SRP completo:** A classe controladora agora tem apenas **um motivo para mudar**: alterações no fluxo geral de coordenação do pedido.
