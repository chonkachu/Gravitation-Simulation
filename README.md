# Trabalho de Física Básica I - Simulação do sistema solar seguindo a lei da gravitação universal 

Integrantes:

Christian Bernard Simas Corrêa Gioia Ribeiro - 11795572

# Documentação da Mecânica Orbital do Sistema Solar

Este documento explica os princípios matemáticos e equações utilizadas na simulação do sistema solar.

## Variáveis Principais

- $M_\odot$ : Massa do Sol
- $m_p$ : Massa do planeta
- $G$ : Constante gravitacional universal
- $r$ : Distância do Sol ao planeta
- $\theta$ : Ângulo em coordenadas polares
- $e$ : Excentricidade orbital
- $r_0$ : Distância do periélio (ponto mais próximo ao Sol)
- $r_{max}$ : Distância do afélio (ponto mais distante do Sol)

## Constantes Fundamentais

$$
G = 6.67430 \times 10^{-11} \text{ m}^3\text{kg}^{-1}\text{s}^{-2}
$$

$$
M_\odot = 1.989 \times 10^{30} \text{ kg}
$$

## Parâmetro Gravitacional

O parâmetro gravitacional K é calculado como:

$$
K = GM_\odot m_p
$$

Isso representa o efeito gravitacional combinado do Sol e do planeta.

## Momento Angular

O momento angular L é uma constante do movimento em problemas de força central e é calculado como:

$$
L = \sqrt{(1 + e)(Km_pr_0)}
$$

onde:
- $e$ é a excentricidade
- $r_0$ é a distância do periélio
- $K$ é o parâmetro gravitacional
- $m_p$ é a massa do planeta

## Posição Orbital

A posição radial do planeta é dada pela equação da órbita:

$$
r(\theta) = \frac{L^2}{Km_p} \cdot \frac{1}{1 + e\cos(\theta)}
$$

Esta é a forma polar da equação da órbita para uma seção cônica, onde:
- $\theta$ é o ângulo a partir do periélio
- $e$ é a excentricidade
- $L$ é o momento angular
- $K$ é o parâmetro gravitacional
- $m_p$ é a massa do planeta

## Período Orbital

O período orbital T é calculado usando a Terceira Lei de Kepler:

T = 2\pi \sqrt{\dfrac{a^3}{GM_\odot}}

onde $a$ é o semi-eixo maior, calculado como:

$$
a = \frac{r_0 + r_{max}}{2}
$$

## Velocidade Angular

A velocidade angular média $\omega$ é calculada a partir do período orbital:

$$
\omega = \frac{2\pi}{T}
$$

## Energia Mecânica

A energia mecânica total E é constante ao longo da órbita e para uma órbita elíptica, a energia total pode ser expressa em termos:

$$
E = -\frac{GM_\odot m_p}{r_0 + r_{max}}
$$

## Coordenadas da Tela

Para exibir as órbitas, convertemos das coordenadas polares $(r,\theta)$ para coordenadas da tela $(x,y)$:

$$
x = \frac{r\cos(\theta)}{escala} + \frac{LARGURA}{2}
$$

$$
y = \frac{r\sin(\theta)}{escala} + \frac{ALTURA}{2}
$$

onde:
- $escala$ é o fator de conversão de metros para pixels
- $LARGURA$ e $ALTURA$ são as dimensões da tela

## Fatores de Escala

A simulação usa os seguintes fatores de escala:
- Escala de distância: $1 \text{ pixel} = 10^9 \text{ metros}$
- Escala de tempo: Ajustável com as teclas de seta, passo de tempo base = $10^5 \text{ segundos}$

Esta escala nos permite visualizar as vastas distâncias no sistema solar dentro das limitações de uma tela de computador, mantendo as proporções corretas das órbitas.
