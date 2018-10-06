# Minimal Pedal Parts
A minimal implementation of a stock keeping system for assembling guitar effects pedals.

## Usage

### Add a part


```shell
python manage.py add_part category value qty
```


```shell
python manage.py add_part resistor 100k 25
```


### Add a pedal

If you do not enter a quantity, it will default to 1.

```shell
python manage.py add_pedal

Enter the pedal name: Old Red Overdive
Enter the parts (press enter twice to finish):
resistor, 100k, 3
resistor, 20k,
capacitor, 100n, 2

Saved Old Red Overdrive
```
You can enter the same part multiple times in the same list. The system will calculate the total for you.

```shell
python manage.py add_pedal

Enter the pedal name: Angry Green Box
Enter the parts (press enter twice to finish):
resistor, 100k 
resistor, 100k 
resistor, 20k
resistor, 100k 

Saved Angry Green Box
```


### Output Missing Part List

Based on the current parts you own, calculates which components you need to purchase to build a pedal.

```shell
python manage.py missing "Angry Green Box"

resistor, 100k, 3
resistor, 20k, 1
```

You can create a parts list for multiple pedals at the same time:

```shell
python manage.py missing "Old Red Overdrive" "Angry Green Box"
```

### Make a Pedal and Update Stock

 ```shell
 python manage.py make "Old Red Overdrive"
 ```

