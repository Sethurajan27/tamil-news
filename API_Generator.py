from playwright.sync_api import sync_playwright

def automate_openai_signup():
    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=True, slow_mo=100)  # Set to True for headless mode
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Go to signup page
        print("🔗 Navigating to OpenAI signup page...")
        page.goto("https://auth.openai.com/create-account")
        print("⏳ Waiting for email field...")
        try:
            page.wait_for_selector('input[type="email"]', timeout=60000)
            print("✉️ Entering email address...")
            page.fill('input[type="email"]', 'user@example.com')
            page.click('button:has-text("Continue")')
        except Exception as e:
            print("❌ Failed to find email field. Possibly blocked or slow page load.")
            print(str(e))
            browser.close()
            return

        # Step 2: Enter password
        print("🔒 Waiting for password field...")
        page.wait_for_url("**/password")

        print("🔐 Entering password...")
        page.fill('input[type="password"]', 'Password1@chatgpt')
        page.click('button:has-text("Continue")')

        # Step 3: Wait for email verification
        print("📨 Waiting for email verification step...")
        page.wait_for_url("**/email-verification")

        # print("🕒 Waiting for user to manually enter the verification code from email...")
        # page.pause()  # Pause so user can enter the OTP manually
        # page.pause()  # Not supported in CI
        print("🚫 Cannot continue without OTP. Skipping this step in CI.")
        return  # Stop script here or simulate

        # Step 4: About You
        print("🧍 Filling out 'About You' section...")
        page.wait_for_url("**/about-you")
        name = 'user@example.com'.split('@')[0]
        name = ''.join(filter(lambda c: not c.isdigit(), name))
        page.fill('input[name="fullName"]', name)
        page.fill('input[name="dob"]', '11-11-1999')
        page.click('button:has-text("Continue")')

        # Step 5: Create Organization
        print("🏢 Creating organization...")
        page.wait_for_url("**/welcome?step=create")
        page.fill('input[name="organizationName"]', 'Personal')
        page.click('button:has-text("Create organization")')

        # Step 6: Invite step
        print("👥 Skipping team invite...")
        page.wait_for_url("**/welcome?step=invite")
        page.click("button:has-text(\"I'll invite my team later\")")

        # Step 7: Try step
        print("🧪 Navigating to API key generation page...")
        page.wait_for_url("**/welcome?step=try")
        page.click('button:has-text("Generate API key")')

        # Final Step: Get the API key
        print("🔑 Retrieving generated API key...")
        page.wait_for_selector('[data-testid="api-key"]')
        api_key = page.inner_text('[data-testid="api-key"]')

        print("\n✅ Successfully generated API Key:")
        print(api_key)

        print("🧹 Closing browser...")
        browser.close()

# Run the automation
automate_openai_signup()
