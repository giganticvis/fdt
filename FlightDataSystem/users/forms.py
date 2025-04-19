from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['date', 'flight_number', 'aircraft_registration', 'flight_crew', 'sn_crew', 'remarks']

class CcdForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    flight = forms.ModelChoiceField(queryset=Flight.objects.none(), label="Select Flight")

    class Meta:
        model = Flight
        fields = ['cabin_crew', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.data:
            try:
                date = self.data.get('date')
                self.fields['flight'].queryset = Flight.objects.filter(date=date)
            except (ValueError, TypeError):
                pass

class OepForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    flight = forms.ModelChoiceField(queryset=Flight.objects.none(), label="Select Flight")

    class Meta:
        model = Flight
        fields = [
            'afl_number', 'from_location', 'to_location', 'air_time_hrs', 'air_time_mins',
            'block_time_hrs', 'block_time_mins', 'fuel_uplift_liters', 'sp_gravity', 'temp_c',
            'fuel_added_kg', 'total_fuel_tons', 'fuel_burnt_tons', 'remaining_fuel_tons',
            'mail_kg', 'cargo_kg', 'pax', 'weight_kg', 'remarks'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.data:
            try:
                date = self.data.get('date')
                self.fields['flight'].queryset = Flight.objects.filter(date=date)
            except (ValueError, TypeError):
                pass
