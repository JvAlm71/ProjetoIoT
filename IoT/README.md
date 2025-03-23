# Projeto de Integração IoT com Eclipse Kura, Eclipse Kapua e ESP32

Este projeto visa criar uma solução de Internet das Coisas (IoT) que utiliza o Eclipse Kura como um broker MQTT local, o Eclipse Kapua como um serviço em nuvem para armazenamento de dados e um ESP32 para coleta e envio de dados de sensores.

## Instalação 

* Clone o repositório por meio, de 
`git clone https://github.com/ICMC-SSC0952-2023/giotgrad03.git`
* Selecione a versão do kapua, exemplo `export IMAGE_VERSION=1.6.7` ou troque todos os lugares que aparecem `{IMAGE_VERSION}` no docker-compose.yml para `1.6.7`
* Execute `docker compose up`
* Faça a configuração do Kura, Kapua e a ESP32 conformes os docs
* Acesse os dados em `localhost:8043`

Após isso, você poderá acessar o Kapua em `localhost:8080` e o Kura `https://localhost:443`. O código para ESP32 está disponivel no arquivo arduino.ino, modifique para refletir sua configuração do Kura e Kapua. Para a instalação da IDE acesse [Instalação do ESP32 no Arduino](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/)

## Autores

| Nome                          | Nusp   | 
|-------------------------------|--------|
| Johnatas Luiz dos Santos      |13676388|
| Aruan Bretas de Oliveira Filho|12609731| 
| João Victor de Almeida        |13695424| 
| Luiz Henrique Benedito        |12563814| 
