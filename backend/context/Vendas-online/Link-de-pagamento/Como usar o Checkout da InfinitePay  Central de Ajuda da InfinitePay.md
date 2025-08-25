Vamos te mostrar como conectar seu site com a InfinitePay de um jeito bem simples! Com essa integração, você vai poder gerar links de pagamento automaticamente e acompanhar as vendas em tempo real.

## **📝 Antes de começar**

Algumas coisinhas importantes que você precisa saber:

## **👉 Acesso**

Para configurar as credenciais necessárias, é só acessar sua conta na web!

## **🔧 Como funciona a integração?**

O processo é bem direto: quando alguém faz um pedido no seu site, você envia os dados para a InfinitePay, recebe um link de pagamento e direciona seu cliente para finalizar a compra. Simples assim!

## **1️⃣ Criando o link de pagamento**

Assim que seu cliente fizer um pedido, você vai enviar uma requisição POST pra gente:

**Dica:** O preço sempre vai em centavos. Então R$ 10,00 = 1000 centavos!

Se você já tem as informações do comprador, pode enviar junto para facilitar o processo:

Se o seu produto precisa ser entregue em mãos, você pode incluir o endereço:

Se tudo der certo, você vai receber uma resposta assim:

Agora é só direcionar seu cliente para essa URL! 🎯

## **2️⃣ Depois que o pagamento acontecer**

Quando seu cliente finalizar o pagamento, ele volta automaticamente pro seu site (na redirect\_url que você configurou). A URL vai vir com alguns parâmetros importantes:

## **3️⃣ Confirmando se o pagamento foi aprovado**

Agora você tem duas opções para verificar se o pagamento realmente aconteceu:

Você pode consultar o status do pagamento fazendo uma requisição:

Se você configurou o webhook\_url, a gente envia os dados da venda automaticamente pro seu sistema:

## **🎯 Como responder ao webhook?**

**Importante:** Responda rapidamente (de preferência em menos de 1 segundo) com um desses códigos:

**✅ Se deu tudo certo:**

❗ **Se algo deu errado:**

**Dica:** Se você responder com erro 400, a gente tenta enviar novamente!

## **💡 Dicas práticas**

Se ficou com alguma dúvida ou encontrou algum problema, nossa equipe está aqui pra te ajudar!

**🔔 Precisa de ajuda?**

Fale com nossa equipe pelo chat no App InfinitePay.

**🔒 Cuide da sua segurança!**

A InfinitePay entra em contato apenas através de canais oficiais e números verificados. Nunca clique em links suspeitos ou compartilhe senhas e códigos de segurança.