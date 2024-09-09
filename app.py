from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def indexIO():
    if request.method == 'POST':
        initial_deposit = float(request.form['initial_deposit'])
        interest_rate = float(request.form['interest_rate'])
        contribution = float(request.form['contribution'])
        compounding_type = request.form['compounding_type']
        time_period_years = int(request.form['time_period_years'])

        n = 12 if compounding_type == 'annually' else 1

        # total amount without contributions (fixed):
        total_amount = initial_deposit * (1 + interest_rate / n) ** (n * time_period_years)

        # total amount with contributions:
        total_contribution = contribution * (((1 + interest_rate / n) ** (n * time_period_years) - 1) / (interest_rate / n))

        final_amount_with_interest = total_amount + total_contribution
        total_contribution_without_interest = initial_deposit + contribution * time_period_years * n
        difference = final_amount_with_interest - total_contribution_without_interest

        amounts_with_interest = []
        amounts_without_interest = []

        years = list(range(time_period_years + 1))

        for year in years:

            year_total_amount = initial_deposit * (1 + interest_rate / n) ** (n * year)
            year_total_contribution = contribution * (((1 + interest_rate / n) ** (n * year) - 1) / (interest_rate / n))

            year_total_contribution_without_interest = initial_deposit + contribution * year * n
            amounts_with_interest.append(year_total_amount + year_total_contribution)
            amounts_without_interest.append(year_total_contribution_without_interest)

        plt.figure(figsize=(10, 5))
        plt.plot(years, amounts_with_interest, marker='o', label='With Interest')
        plt.plot(years, amounts_without_interest, marker='o', label='Without Interest')
        plt.title('Compound Interest Over Time Comparison')
        plt.xlabel('Years')
        plt.ylabel('Amount ($)')
        plt.grid(True)
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('result.html', final_amount=final_amount_with_interest, difference=difference, plot_url=plot_url)


    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
