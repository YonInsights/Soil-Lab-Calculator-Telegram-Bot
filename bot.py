from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from calculations import *  # Importing all functions from calculations.py

# Global dictionary to store user session data
user_data = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_menu = [
        ["Moisture Content 🌧️", "Atterberg Limits 🧪"],
        ["Shrinkage Limit 🪓", "Linear Shrinkage 📏"],
        ["Hydrometer Analysis 🌡️", "CBR Test 🚜"],
        ["Material Finer No. 200 📊", "Specific Gravity ⚖️"],
        ["Moisture Density Relationship 💧", "Volume Metric 📐"],
    ]
    await update.message.reply_text(
        "👋 Welcome to the *Soil Property Calculator Bot*! \n\n"
        "🌱 Select a property to calculate from the options below:",
        reply_markup=ReplyKeyboardMarkup(main_menu, one_time_keyboard=True, resize_keyboard=True),
        parse_mode="Markdown",
    )

# Menu selection handler
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_choice = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id]['test'] = user_choice

    # Prompt for specific test inputs
    if user_choice == "Moisture Content 🌧️":
        user_data[user_id]['state'] = 'awaiting_wet_weight'
        await update.message.reply_text("🧪 *Moisture Content*: Enter the *wet weight (grams)*:", parse_mode="Markdown")

    elif user_choice == "Atterberg Limits 🧪":
        user_data[user_id]['state'] = 'awaiting_liquid_limit'
        await update.message.reply_text("🧪 *Atterberg Limits*: Enter the *Liquid Limit (%)*:", parse_mode="Markdown")

    elif user_choice == "Shrinkage Limit 🪓":
        user_data[user_id]['state'] = 'awaiting_initial_volume'
        await update.message.reply_text("🪓 *Shrinkage Limit*: Enter the *initial volume (cm³)*:", parse_mode="Markdown")

    elif user_choice == "Linear Shrinkage 📏":
        user_data[user_id]['state'] = 'awaiting_initial_length'
        await update.message.reply_text("📏 *Linear Shrinkage*: Enter the *initial length (cm)*:", parse_mode="Markdown")

    elif user_choice == "CBR Test 🚜":
        user_data[user_id]['state'] = 'awaiting_force_applied'
        await update.message.reply_text("🚜 *CBR Test*: Enter the *force applied (kN)*:", parse_mode="Markdown")

    elif user_choice == "Hydrometer Analysis 🌡️":
        user_data[user_id]['state'] = 'awaiting_penetration_depth'
        await update.message.reply_text("🌡️ *Hydrometer Analysis*: Enter the *penetration depth (mm)*:", parse_mode="Markdown")

    elif user_choice == "Material Finer No. 200 📊":
        user_data[user_id]['state'] = 'awaiting_initial_mass'
        await update.message.reply_text("📊 *Material Finer No. 200*: Enter the *initial mass (grams)*:", parse_mode="Markdown")

    elif user_choice == "Specific Gravity ⚖️":
        user_data[user_id]['state'] = 'awaiting_mass_of_dry_soil'
        await update.message.reply_text("⚖️ *Specific Gravity*: Enter the *mass of dry soil (grams)*:", parse_mode="Markdown")

    elif user_choice == "Moisture Density Relationship 💧":
        user_data[user_id]['state'] = 'awaiting_dry_density'
        await update.message.reply_text("💧 *Moisture Density Relationship*: Enter the *dry density (g/cm³)*:", parse_mode="Markdown")

    elif user_choice == "Volume Metric 📐":
        user_data[user_id]['state'] = 'awaiting_initial_volume_for_metric'
        await update.message.reply_text("📐 *Volume Metric*: Enter the *initial volume (cm³)*:", parse_mode="Markdown")

# Input handling for each test
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data:
        await update.message.reply_text("Please start again using /start.")
        return

    user_session = user_data[user_id]

    # Moisture Content
    if user_session.get('test') == "Moisture Content 🌧️":
        if user_session.get('state') == 'awaiting_wet_weight':
            try:
                wet_weight = float(update.message.text)
                user_session['wet_weight'] = wet_weight
                user_session['state'] = 'awaiting_dry_weight'
                await update.message.reply_text("Enter the *dry weight (grams)*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for wet weight.")
        elif user_session.get('state') == 'awaiting_dry_weight':
            try:
                dry_weight = float(update.message.text)
                wet_weight = user_session.get('wet_weight')
                result = calculate_moisture_content(wet_weight, dry_weight)
                await update.message.reply_text(f"✅ *Moisture Content*: *{result:.2f}%*", parse_mode="Markdown")
                user_data.pop(user_id, None)  # Clear session after calculation
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for dry weight.")

    # Atterberg Limits
    elif user_session.get('test') == "Atterberg Limits 🧪":
        if user_session.get('state') == 'awaiting_liquid_limit':
            try:
                liquid_limit = float(update.message.text)
                user_session['liquid_limit'] = liquid_limit
                user_session['state'] = 'awaiting_plastic_limit'
                await update.message.reply_text("Enter the *Plastic Limit (%)*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for Liquid Limit.")
        elif user_session.get('state') == 'awaiting_plastic_limit':
            try:
                plastic_limit = float(update.message.text)
                liquid_limit = user_session.get('liquid_limit')
                result = calculate_plasticity_index(liquid_limit, plastic_limit)
                await update.message.reply_text(f"✅ *Plasticity Index*: *{result:.2f}*", parse_mode="Markdown")
                user_data.pop(user_id, None)
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for Plastic Limit.")

    # CBR Test 🚜
    elif user_session.get('test') == "CBR Test 🚜":
        if user_session.get('state') == 'awaiting_force_applied':
            try:
                force_applied = float(update.message.text)
                user_session['force_applied'] = force_applied
                user_session['state'] = 'awaiting_standard_force'
                await update.message.reply_text("Enter the *standard force (kN)*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for force applied.")
        elif user_session.get('state') == 'awaiting_standard_force':
            try:
                standard_force = float(update.message.text)
                force_applied = user_session.get('force_applied')
                result = calculate_cbr(force_applied, standard_force)
                await update.message.reply_text(f"✅ *CBR Test Result*: *{result:.2f}%*", parse_mode="Markdown")
                user_data.pop(user_id, None)
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for standard force.")

    # Specific Gravity ⚖️
    elif user_session.get('test') == "Specific Gravity ⚖️":
        if user_session.get('state') == 'awaiting_mass_of_dry_soil':
            try:
                mass_of_dry_soil = float(update.message.text)
                user_session['mass_of_dry_soil'] = mass_of_dry_soil
                user_session['state'] = 'awaiting_mass_of_displaced_water'
                await update.message.reply_text("Enter the *mass of displaced water (grams)*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for mass of dry soil.")
        elif user_session.get('state') == 'awaiting_mass_of_displaced_water':
            try:
                mass_of_displaced_water = float(update.message.text)
                mass_of_dry_soil = user_session.get('mass_of_dry_soil')
                result = calculate_specific_gravity(mass_of_dry_soil, mass_of_displaced_water)
                await update.message.reply_text(f"✅ *Specific Gravity*: *{result:.2f}*", parse_mode="Markdown")
                user_data.pop(user_id, None)
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for mass of displaced water.")

    # Hydrometer Analysis 🌡️
    elif user_session.get('test') == "Hydrometer Analysis 🌡️":
        if user_session.get('state') == 'awaiting_penetration_depth':
            try:
                penetration_depth = float(update.message.text)
                user_session['penetration_depth'] = penetration_depth
                user_session['state'] = 'awaiting_fluid_viscosity'
                await update.message.reply_text("Enter the *fluid viscosity (Pa·s)*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for penetration depth.")

        elif user_session.get('state') == 'awaiting_fluid_viscosity':
            try:
                fluid_viscosity = float(update.message.text)
                user_session['fluid_viscosity'] = fluid_viscosity
                user_session['state'] = 'awaiting_specific_gravity'
                await update.message.reply_text("Enter the *specific gravity of soil particles*:", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for fluid viscosity.")

        elif user_session.get('state') == 'awaiting_specific_gravity':
            try:
                specific_gravity = float(update.message.text)
                penetration_depth = user_session.get('penetration_depth')
                fluid_viscosity = user_session.get('fluid_viscosity')
                
                # Perform the calculation
                result = calculate_hydrometer(penetration_depth, fluid_viscosity, specific_gravity)
                
                await update.message.reply_text(
                    f"✅ *Hydrometer Analysis Result*: Particle Diameter = *{result:.2f} mm*",
                    parse_mode="Markdown"
                )
                user_data.pop(user_id, None)  # Clear session data after calculation
            except ValueError:
                await update.message.reply_text("❌ Invalid input. Enter a valid *number* for specific gravity.")

# Error handler for unexpected inputs
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again.")

# Main function to run the bot
def main():
    application = Application.builder().token("7612086349:AAEme1YLN2pUZ72C9flAaIwSmHLtpGobd30").build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'^(Moisture Content 🌧️|Atterberg Limits 🧪|Shrinkage Limit 🪓|Linear Shrinkage 📏|Hydrometer Analysis 🌡️|CBR Test 🚜|Material Finer No. 200 📊|Specific Gravity ⚖️|Moisture Density Relationship 💧|Volume Metric 📐)$'), handle_menu_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    application.add_handler(MessageHandler(filters.ALL, error))  # Catch-all error handler

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
