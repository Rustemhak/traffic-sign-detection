# Проект по глубокому обучение на практике от **команды ** - **Распознавание и классификация дорожных знаков**


## Демо-приложение доступно по [cсылке](http://51.250.120.151:8501/), развернуто на Yandex Cloud
## Как запустить локально
- `docker build -t streamlit .`
- `docker run -p 8501:8501 streamlit`
- переходим на http://0.0.0.0:8501


### 1. Формализация задачи

**Задача:** Разработать систему распознавания и классификации дорожных знаков, которая будет анализировать видео с видеорегистратора и оповещать водителя о дорожных знаках в режиме реального времени.

**Требования:**
- Высокая точность распознавания (precision >= 90%, recall >= 90%).
- Работа в различных условиях (освещение, погода).
- Поддержка разнообразных знаков (ограничения скорости, запреты, предупреждения).

### 2. Датасет и классы
* [Датасет по детекции](https://www.kaggle.com/datasets/watchman/rtsd-dataset)
* [Датасет по классиификации](https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign)
* [Датасеты в Roboflow](https://universe.roboflow.com/ilya-stmnk/road-mnsrr)
  - Задача классификации одного изображения по нескольким классам
  - Более 40 классов
  - Всего более 50 000 изображений
  - Большая, реалистичная база данных

### 3. Формулировка задачи в ML-терминах

**Метрики:**
- mAP
- Precision и Recall, 
- Время обработки кадра (для оценки способности работать в реальном времени - 5ms).

**Архитектуры:**
- [yolo-8-nano](https://github.com/Rustemhak/dl-pract-ai-talent-hub/blob/main/road.ipynb)
-  [RT-DETR](https://docs.ultralytics.com/models/rtdetr/)
- Рассмотрение подходов сегментации, если требуется точное выделение знаков на изображении.
**Эксперименты**
  - ClearML
**Версионирование датасетов**
  - Roboflow

### 4. Архитектура решения
![Архитектура решения](https://github.com/Rustemhak/dl-pract-ai-talent-hub/blob/main/architecture.jpg)

### 5. Сравнение моделей

Сравнение метрик YOLOv8 и RT-DETR (с лучшими гиперпараметрами)

| model   | precision | recall | mAP50|speed(ms)
|---------|-----------|--------|------|-----|
 | YOLOv8  | 0.98      | 0.96   |0.975| 5|
 | RT-DETR |0.97|0.97|0.985|17.5|

#### График метрик YOLOv8
![График метрик YOLOv8](https://github.com/Rustemhak/dl-pract-ai-talent-hub/blob/main//metrics/metrics_YOLOv8.png)
#### График метрик RT-DETR
![График метрик RT-DETR](https://github.com/Rustemhak/dl-pract-ai-talent-hub/blob/main//metrics/metrics_RT-DETR.png)
#### Сравнение метрик в ClearML
![Сравнение метрик в ClearML](https://github.com/Rustemhak/dl-pract-ai-talent-hub/blob/main//metrics/ClearML_comparsion.png)

Взяли YOLOv8, так как имеет схожие метрики precision, recall и mAP с RT-DETR, но сильно выигрывает по скорости работы
<details>
 <summary>Подробное сравнение RT-DETR с разными оптимизаторами </summary>

model | precision | recall | mAP50 |speed(ms)
----|-------|---|-------|----
SGD |0.963|0.981| 0.989 |17.5
AdamW|0.971|0.968|0.985|17.5

</details>

## Состав команды
- [Рустем Хакимуллин](https://github.com/Rustemhak)
- [Даниил Маргарян](https://github.com/DanilMargaryan)
- [Илья Шушарин](https://github.com/AzekAriman)
- [Марат Кузьмин](https://github.com/soaptr)