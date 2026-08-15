import { expect, test } from "@playwright/test";

const showcase = "/showcase/modular-desk-lamp/index.html";

function captureRuntimeErrors(page) {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

test.describe("desktop lightweight runtime", () => {
  test("mounts only the active page window and supports navigation", async ({ page, isMobile }) => {
    test.skip(isMobile, "Desktop navigation controls are intentionally hidden on mobile.");
    const errors = captureRuntimeErrors(page);
    await page.goto(showcase);

    const slides = page.locator(".slide");
    await expect(slides).toHaveCount(14);
    await expect(page.locator("html")).toHaveAttribute("data-style", "instrument-blue");
    await expect(page.locator("#counter")).toHaveText("01 / 14");
    await expect(slides.nth(0)).toHaveClass(/is-active/);

    const mountedAtStart = await page.locator('.slide[data-mounted="true"]').count();
    expect(mountedAtStart).toBeLessThanOrEqual(2);
    expect(await slides.nth(3).innerHTML()).toBe("");

    await page.locator("#next").click();
    await expect(page.locator("#counter")).toHaveText("02 / 14");
    await expect(slides.nth(1)).toHaveClass(/is-active/);
    const accentContrast = await slides.nth(1).evaluate((slide) => {
      const parse = (value) => value.match(/[\d.]+/g).slice(0, 3).map(Number);
      const luminance = (value) => {
        const channels = parse(value).map((channel) => channel / 255).map(
          (channel) => channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4,
        );
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
      };
      const foreground = luminance(getComputedStyle(slide.querySelector(".eyebrow")).color);
      const background = luminance(getComputedStyle(slide).backgroundColor);
      return (Math.max(foreground, background) + 0.05) / (Math.min(foreground, background) + 0.05);
    });
    expect(accentContrast).toBeGreaterThanOrEqual(4.5);

    await page.keyboard.press("End");
    await expect(page.locator("#counter")).toHaveText("14 / 14");
    expect(await slides.nth(0).innerHTML()).toBe("");
    expect(await page.locator('.slide[data-mounted="true"]').count()).toBeLessThanOrEqual(2);
    expect(errors).toEqual([]);
  });

  test("opens a requested page directly", async ({ page, isMobile }) => {
    test.skip(isMobile, "Covered by the mobile-specific direct-page test.");
    await page.goto(`${showcase}?page=4`);
    await expect(page.locator("#counter")).toHaveText("04 / 14");
    await expect(page.locator(".slide").nth(3)).toHaveClass(/is-active/);
    expect(await page.locator('.slide[data-mounted="true"]').count()).toBeLessThanOrEqual(3);
  });

  test("hydrates all pages for print and export", async ({ page, isMobile }) => {
    test.skip(isMobile, "The export path is viewport-independent and covered on desktop.");
    const errors = captureRuntimeErrors(page);
    await page.goto(`${showcase}?render=all`);
    await expect(page.locator("html")).toHaveClass(/render-all/);
    await expect(page.locator('.slide[data-mounted="true"]')).toHaveCount(14);

    const deferredImages = page.locator("img[data-src]");
    expect(await deferredImages.count()).toBeGreaterThan(0);
    await expect(deferredImages.first()).toHaveAttribute("src", /\.webp$/);
    expect(await deferredImages.evaluateAll((images) => images.every((image) => image.currentSrc.endsWith(".webp")))).toBe(true);
    expect(errors).toEqual([]);
  });

  test("hydrates before printing and restores the lightweight window afterward", async ({ page, isMobile }) => {
    test.skip(isMobile, "Desktop print lifecycle is sufficient for the shared runtime.");
    await page.goto(`${showcase}?page=6`);
    await page.evaluate(() => dispatchEvent(new Event("beforeprint")));
    await expect(page.locator('.slide[data-mounted="true"]')).toHaveCount(14);
    await page.evaluate(() => dispatchEvent(new Event("afterprint")));
    expect(await page.locator('.slide[data-mounted="true"]').count()).toBeLessThanOrEqual(3);
  });
});

test.describe("mobile runtime", () => {
  test("uses vertical layout and loads the requested page neighborhood", async ({ page, isMobile }) => {
    test.skip(!isMobile, "This assertion targets the mobile layout.");
    const errors = captureRuntimeErrors(page);
    await page.goto(`${showcase}?page=4`);
    await expect(page.locator("#counter")).toHaveText("04 / 14");

    const deckDisplay = await page.locator("#deck").evaluate((element) => getComputedStyle(element).display);
    expect(deckDisplay).toBe("block");
    await expect(page.locator(".slide").nth(3)).toHaveAttribute("data-mounted", "true");
    expect(await page.locator('.slide[data-mounted="true"]').count()).toBeLessThan(14);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
    expect(errors).toEqual([]);
  });
});
