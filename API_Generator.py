from playwright.sync_api import sync_playwright

def automate_openai_signup():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True, slow_mo=100)  # Visible browser
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Go to signup page
        print("Navigating to OpenAI signup page...")
        page.goto("https://auth.openai.com/create-account")

        print("Waiting for email field...")
        try:
            page.wait_for_selector('input[type="email"]', timeout=60000)
            print("Entering email address...")
            page.fill('input[type="email"]', 'jopogi4977@2mik.com')
            page.click('button:has-text("Continue")')
        except Exception as e:
            print("Failed to find email field. Possibly blocked.")
            print(str(e))
            browser.close()
            return

        # Step 2: Password
        print("Waiting for password field...")
        page.wait_for_url("**/password", timeout=60000)
        print("Entering password...")
        page.fill('input[type="password"]', 'Password1@chatgpt')
        page.click('button:has-text("Continue")')

        # Step 3: OTP
        print("Waiting for email verification...")
        page.wait_for_url("**/email-verification", timeout=60000)
        print("Please enter OTP manually and click continue.")
        page.pause()

        # Step 4: About You
        print("Filling out 'About You'...")
        page.wait_for_url("**/about-you", timeout=60000)
        name = ''.join(filter(lambda c: not c.isdigit(), 'jopogi4977@2mik.com'.split('@')[0]))
        page.fill('input[name="fullName"]', name)
        page.fill('input[name="dob"]', '11-11-1999')
        page.click('button:has-text("Continue")')

        # Step 5: Create Organization
        print("Creating organization...")
        page.wait_for_url("**/welcome?step=create", timeout=60000)
        page.fill('input[name="organizationName"]', 'Personal')
        page.click('button:has-text("Create organization")')

        # Step 6: Skip Invite
        print("Skipping invite step...")
        page.wait_for_url("**/welcome?step=invite", timeout=60000)
        page.click("button:has-text(\"I'll invite my team later\")")

        # Step 7: Generate API key
        print("Navigating to API key generation...")
        page.wait_for_url("**/welcome?step=try", timeout=60000)
        page.click('button:has-text("Generate API key")')

        print("Waiting for API key...")
        page.wait_for_selector('[data-testid="api-key"]', timeout=60000)
        api_key = page.inner_text('[data-testid="api-key"]')
        print(f"\nYour API Key: {api_key}")

        print("Closing browser...")
        browser.close()

automate_openai_signup()
