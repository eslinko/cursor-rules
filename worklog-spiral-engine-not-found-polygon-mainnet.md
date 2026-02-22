# Worklog: SpiralEngine не находится при запуске на Polygon mainnet

**Дата:** 2026-01-26  
**Задача:** Диагностика «SpiralEngine не находится» при Action 5 / Action 777 на Polygon  
**Методология:** @hypothesis-driven-error-analysis.md  
**Проблема:** В деплое/инвайтах на Polygon mainnet SpiralEngine не находится, хотя в реестре mainnet он зарегистрирован.

---

## 1. Описание ошибки

### Симптомы

- При запуске **Action 5** на Polygon: путь **deploy** (не upgrade), в логах — «MagicRegistry not found» или адрес SpiralEngine не подставляется из реестра.
- При запуске **Action 777** или загрузке SpiralEngine: ошибка вида «SpiralEngine не найден» / «Proxy адрес не найден… ни в .env, ни в MagicRegistry для SpiralEngine».
- Ожидание: при `--network polygon` и корректном .env адрес SpiralEngine должен браться из MagicRegistry mainnet (0x6a3d3e…).

### Контекст

- **Компонент:** `scripts/lib/services/ContractManager.js` — `loadUUPSContract('SpiralEngine')`, `_getOrLoadSpiralEngine()`; загрузка MagicRegistry из `process.env.MAGIC_REGISTRY_CONTRACT_ADDRESS`.
- **Входные данные:** .env (или env.mainnet) — `MAGIC_REGISTRY_CONTRACT_ADDRESS`, `SPIRAL_ENGINE_CONTRACT_ADDRESS`, `RPC_URL`; сеть — Polygon mainnet.
- **Условия воспроизведения:** `npx hardhat run scripts/deploy_full.js --network polygon` с Action 5 или 777; либо вызов `contractManager.loadUUPSContract('SpiralEngine')` без предзаполненного кеша.

### Факты из предыдущего анализа (action5-action777-receipt-pending-analysis-2026-01-31.md)

- Action 5 пошёл по пути **deploy** (не upgrade) → `checkExistingContract` вернул null или в конфиге не было адреса SpiralEngine.
- В логах: «MagicRegistry not found» — загрузка MagicRegistry не удалась или не выполнялась с нужным адресом.

---

## 2. Анализ возможных источников проблемы

### 2.1 Неверный или локальный MAGIC_REGISTRY_CONTRACT_ADDRESS в .env при запуске на Polygon

**Гипотеза:** При запуске на Polygon в .env указан адрес реестра от другой сети (например, локальный Anvil `0x36b58F5C…`). Код загружает контракт по этому адресу **через RPC Polygon**. На Polygon по адресу `0x36b58…` находится другой контракт (или пусто) → вызов `get('SpiralEngine')` ревертится или возвращает zero → «SpiralEngine не находится».

**Обоснование:**

- В коде адрес реестра берётся только из `process.env.MAGIC_REGISTRY_CONTRACT_ADDRESS` (и кеша); сеть задаётся RPC, а не отдельным «профилем».
- Если в .env скопирован адрес с localhost, при `--network polygon` RPC = Polygon, но адрес реестра остаётся локальным → на Polygon по этому адресу не тот реестр.

**Вероятность:** Высокая  
**Влияние:** P0 (блокирует загрузку SpiralEngine и выбор upgrade path в Action 5)

### 2.2 SpiralEngine отсутствует в реестре mainnet

**Гипотеза:** В реестре Polygon mainnet (0x6a3d3e…) нет ключа SpiralEngine или он zero.

**Обоснование:** Тогда при корректном MAGIC_REGISTRY_CONTRACT_ADDRESS вызов `magicRegistry.get('SpiralEngine')` вернул бы zero или реверт.

**Вероятность:** Низкая (после проверки — опровергнута)  
**Влияние:** P0

### 2.3 Имя ключа в реестре отличается от "SpiralEngine"

**Гипотеза:** В контракте реестр хранит ключ в другом формате (например, "SpiralEngineProxy"), а код вызывает `get('SpiralEngine')`.

**Обоснование:** В коде везде используется `magicRegistry.get('SpiralEngine')` и `get(contractName)` с именами из SUPPORTED_CONTRACTS; в деплое запись идёт как `set(contractName, address)` с тем же именем.

**Вероятность:** Низкая  
**Влияние:** P0

---

## 3. Тест гипотез (запрос реестра mainnet)

### 3.1 Цель теста

- Проверить, что в реестре **Polygon mainnet** по адресу `0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576` есть ключ `SpiralEngine` и непустой адрес.
- Убедиться, что при использовании этого же адреса реестра и RPC Polygon SpiralEngine «находится».

### 3.2 Метод

- Скрипт `scripts/utility/query_magic_registry.js` с профилем mainnet (константы в скрипте: RPC `https://polygon-rpc.com`, MagicRegistry `0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576`).
- Запуск: `node scripts/utility/query_magic_registry.js --mainnet`.

### 3.3 Результаты теста (2026-01-26)

```
Profile: mainnet
MagicRegistry: 0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576
RPC: https://polygon-rpc.com

Key                          | Address
-----------------------------|------------------------------------------
SpiralEngine                 | 0xE5C54Fe5f2bc28555662c107a3a6b23D028c2bDb
SoulboundCore                | 0xe1a53255294c318d0876F4d6EE8a66726303422D
SoulMetadata                 | 0xe2B30Ca066E20709C88f8BD1E02dC277742E3394
SoulRecovery                 | 0x889DE583b7c5f6f3EF1918622784C6962ef2cE0c
SoulIntegration              | 0x4F60357BB6C2C92ABe7dFeD5a4E17a78072267Bd
SoulIdentity                 | (error: rate limit / missing response — RPC)
ProductRegistry              | (error: rate limit / missing response — RPC)
OrganicComponentRegistry     | (error: rate limit / missing response — RPC)
AmanitaInternational         | 0x2664B2D61DAc224b3A160b1Ef211fd3C157a7F14
```

**Вывод по гипотезам:**

- **2.2 опровергнута:** SpiralEngine **есть** в реестре mainnet, адрес `0xE5C54Fe5f2bc28555662c107a3a6b23D028c2bDb`.
- **2.3 опровергнута:** Ключ в реестре — именно `SpiralEngine`, имя совпадает с кодом.
- **2.1 остаётся наиболее вероятной:** Проблема не в том, что SpiralEngine нет в реестре, а в том, что при запуске деплоя/инвайтов на Polygon в .env использовался **другой** адрес MagicRegistry (например, локальный), поэтому код обращался не к mainnet-реестру и не получал SpiralEngine.

---

## 4. Анализ кода (источник адреса реестра и SpiralEngine)

- **ContractManager.loadUUPSContract('SpiralEngine'):**  
  Сначала `process.env.SPIRAL_ENGINE_PROXY_ADDRESS` / `SPIRAL_ENGINE_CONTRACT_ADDRESS`. Если нет — загружается MagicRegistry по `process.env.MAGIC_REGISTRY_CONTRACT_ADDRESS`, затем `magicRegistry.get('SpiralEngine')`. Если реестр не загружен (адрес не задан или неверный) или вызов `get` падает — выбрасывается «Proxy адрес не найден… ни в .env, ни в MagicRegistry для SpiralEngine».

- **ContractManager._getOrLoadSpiralEngine():**  
  Аналогично: кеш → `config.getContractAddress('SpiralEngine')` → при отсутствии загрузка MagicRegistry по `config.getContractAddress('MagicRegistry')` или `process.env.MAGIC_REGISTRY_CONTRACT_ADDRESS`, затем `magicRegistry.get('SpiralEngine')`.

- **Итог:** Единственный источник адреса реестра в рантайме — `.env` (и кеш). Профиль сети (localhost vs polygon) задаётся RPC (Hardhat `--network`), а не отдельным переключателем для адресов контрактов. Поэтому при запуске на Polygon с .env от localhost реестр на Polygon будет запрошен по локальному адресу → не тот контракт → SpiralEngine не находится.

---

## 5. Рекомендуемое решение

### Решение 1: Использовать env.mainnet при запуске на Polygon (приоритет P0)

**Действие:** При выполнении Action 5 / 777 или любых скриптов на Polygon mainnet подставлять переменные из **env.mainnet** (или его копии в .env), где заданы:

- `MAGIC_REGISTRY_CONTRACT_ADDRESS=0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576`
- `SPIRAL_ENGINE_CONTRACT_ADDRESS=0xE5C54Fe5f2bc28555662c107a3a6b23D028c2bDb` (опционально, можно брать из реестра)
- RPC для Polygon (например, `RPC_URL` или `POLYGON_MAINNET_RPC`)

**Пример запуска:**

```bash
# Вариант 1: подставить env.mainnet в .env перед запуском
cp env.mainnet .env
npx hardhat run scripts/deploy_full.js --network polygon

# Вариант 2: явно задать только реестр для текущего запуска
MAGIC_REGISTRY_CONTRACT_ADDRESS=0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576 npx hardhat run scripts/deploy_full.js --network polygon
```

**Преимущества:**

- SpiralEngine будет найден через реестр mainnet (или напрямую из .env).
- Action 5 сможет выбрать путь upgrade, если в .env также задан `SPIRAL_ENGINE_CONTRACT_ADDRESS` и контракт уже существует.

### Решение 2 (улучшение): Профиль сети по --network

**Идея:** В конфиге или скриптах по `--network polygon` подставлять адрес реестра (и при необходимости RPC) из заранее заданного профиля (constants или config по имени сети), чтобы не зависеть от того, какой .env сейчас загружен. Требует доработки конфига/деплой-скриптов.

---

## 6. Вывод

1. **SpiralEngine в mainnet реестре есть:** ключ `SpiralEngine`, адрес `0xE5C54Fe5f2bc28555662c107a3a6b23D028c2bDb` (подтверждено `query_magic_registry.js --mainnet`).
2. **Причина «SpiralEngine не находится»** при запуске на Polygon — использование в .env адреса MagicRegistry от другой сети (например, локального). На Polygon по такому адресу запрашивается не тот реестр, и `get('SpiralEngine')` не возвращает корректный адрес.
3. **Рекомендация:** Для Polygon mainnet использовать `env.mainnet` (или те же значения в .env): `MAGIC_REGISTRY_CONTRACT_ADDRESS=0x6a3d3e2328e9D613a6F9cf42FF1fBa655fc71576` и при необходимости явно задавать его при запуске, если .env по умолчанию от другой сети.

---

**Версия:** 1.0  
**Статус:** Гипотеза 2.1 подтверждена косвенно (2.2 и 2.3 опровергнуты тестом); решение 1 применимо без изменений кода.
