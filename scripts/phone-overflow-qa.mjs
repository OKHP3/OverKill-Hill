#!/usr/bin/env node
/**
 * Phone overflow QA
 * =================
 * Browser-level regression check for the site's widest public content.
 *
 * Opens representative pages at 320px and fails when:
 * - the document is horizontally scrollable;
 * - a table is not contained by a scrollable table wrapper;
 * - a table's rightmost column cannot be revealed by scrolling its wrapper; or
 * - a diagram grid or one of its cards extends outside the viewport.
 *
 * Usage:
 *   npm run test:phone-overflow
 *   node scripts/phone-overflow-qa.mjs --base-url http://127.0.0.1:5000
 */

import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const DEFAULT_BASE_URL = 'http://127.0.0.1:5000';
const baseArg = process.argv.find((arg) => arg.startsWith('--base-url='));
const baseUrl = (baseArg ? baseArg.slice('--base-url='.length) : DEFAULT_BASE_URL)
  .replace(/\/$/, '');

const VIEWPORT = { width: 320, height: 800 };
const TABLE_WRAPPER_SELECTOR = '.data-table-wrap, .table-scroll-wrap';
const WIDE_TABLE_SELECTOR = '.data-table, .schedule-table, .gen-table';

const PAGES = [
  {
    name: 'manifesto',
    path: '/manifesto/',
    expect: { tables: 1, diagramGrids: 0 },
  },
  {
    name: 'mac-studio-local-ai-workbench',
    path: '/projects/mac-studio-local-ai-workbench/',
    expect: { tables: 3, diagramGrids: 0 },
  },
  {
    name: 'first-diagram-is-a-liar',
    path: '/writings/first-diagram-is-a-liar/',
    expect: { tables: 2, diagramGrids: 3 },
  },
];

function printFailure(pageName, message) {
  console.error(`FAIL  ${pageName}: ${message}`);
}

function configureNixBrowserCompatibility() {
  // Replit's Nix host can omit libgbm even though Chromium runs headlessly with
  // GPU disabled. Keep the shim outside the repository and load it only for the
  // child Chromium process. Ubuntu CI uses its normal browser dependencies.
  const shimDir = join(tmpdir(), 'okh-playwright-libs');
  const shimPath = join(shimDir, 'libgbm.so.1');
  mkdirSync(shimDir, { recursive: true });
  const sourcePath = join(shimDir, 'libgbm-shim.c');
  writeFileSync(
    sourcePath,
    [
      '#include <stdint.h>',
      'typedef struct gbm_device gbm_device;',
      'typedef struct gbm_bo gbm_bo;',
      'gbm_device *gbm_create_device(int fd) { return 0; }',
      'void gbm_device_destroy(gbm_device *device) {}',
      'int gbm_device_get_fd(gbm_device *device) { return -1; }',
      'int gbm_device_is_format_supported(gbm_device *device, uint32_t format, uint32_t usage) { return 0; }',
      'gbm_bo *gbm_bo_create(gbm_device *device, uint32_t width, uint32_t height, uint32_t format, uint32_t flags) { return 0; }',
      'gbm_bo *gbm_bo_create_with_modifiers(gbm_device *device, uint32_t width, uint32_t height, uint32_t format, const uint64_t *modifiers, uint32_t count) { return 0; }',
      'gbm_bo *gbm_bo_import(gbm_device *device, uint32_t type, void *buffer, uint32_t usage) { return 0; }',
      'void gbm_bo_destroy(gbm_bo *buffer) {}',
      'gbm_device *gbm_bo_get_device(gbm_bo *buffer) { return 0; }',
      'int gbm_bo_get_fd_for_plane(gbm_bo *buffer, int plane) { return -1; }',
      'uint64_t gbm_bo_get_handle(gbm_bo *buffer) { return 0; }',
      'uint64_t gbm_bo_get_handle_for_plane(gbm_bo *buffer, int plane) { return 0; }',
      'uint32_t gbm_bo_get_height(gbm_bo *buffer) { return 0; }',
      'uint64_t gbm_bo_get_modifier(gbm_bo *buffer) { return 0; }',
      'uint32_t gbm_bo_get_offset(gbm_bo *buffer, int plane) { return 0; }',
      'int gbm_bo_get_plane_count(gbm_bo *buffer) { return 0; }',
      'uint32_t gbm_bo_get_stride_for_plane(gbm_bo *buffer, int plane) { return 0; }',
      'uint32_t gbm_bo_get_width(gbm_bo *buffer) { return 0; }',
      'void *gbm_bo_map(gbm_bo *buffer, uint32_t x, uint32_t y, uint32_t width, uint32_t height, uint32_t flags, uint32_t *stride, void **data) { return 0; }',
      'void gbm_bo_unmap(gbm_bo *buffer, void *data) {}',
    ].join('\n'),
  );
  execFileSync('gcc', [
    '-shared',
    '-fPIC',
    '-Wl,-soname,libgbm.so.1',
    '-o',
    shimPath,
    sourcePath,
  ]);
  process.env.LD_LIBRARY_PATH = [shimDir, process.env.LD_LIBRARY_PATH]
    .filter(Boolean)
    .join(':');
}

async function inspectPage(page, definition) {
  const response = await page.goto(`${baseUrl}${definition.path}`, {
    waitUntil: 'domcontentloaded',
    timeout: 30_000,
  });

  const failures = [];
  if (!response || response.status() >= 400) {
    failures.push(`HTTP ${response?.status() ?? 'no response'}`);
    return failures;
  }

  const report = await page.evaluate(
    ({ tableWrapperSelector, wideTableSelector, expected }) => {
      const tolerance = 1;
      const viewportWidth = window.innerWidth;
      const documentWidth = Math.max(
        document.documentElement.scrollWidth,
        document.body.scrollWidth,
      );

      const tables = Array.from(document.querySelectorAll(wideTableSelector)).map((table, index) => {
        const wrapper = table.closest(tableWrapperSelector);
        if (!wrapper) {
          return { index, wrapperFound: false };
        }

        const wrapperRect = wrapper.getBoundingClientRect();
        const lastRow = table.rows[table.rows.length - 1];
        const lastCell = lastRow?.cells[lastRow.cells.length - 1];
        const initialScrollLeft = wrapper.scrollLeft;
        wrapper.scrollLeft = wrapper.scrollWidth;
        const lastCellRect = lastCell?.getBoundingClientRect();
        const finalColumnVisible = Boolean(
          lastCellRect
          && lastCellRect.right <= wrapperRect.right + tolerance
          && lastCellRect.right > wrapperRect.left + tolerance
        );
        const wrapperScrollable = wrapper.scrollWidth > wrapper.clientWidth + tolerance;
        wrapper.scrollLeft = initialScrollLeft;

        return {
          index,
          wrapperFound: true,
          wrapperScrollable,
          wrapperWithinViewport:
            wrapperRect.left >= -tolerance
            && wrapperRect.right <= viewportWidth + tolerance,
          finalColumnVisible,
          columns: table.rows[0]?.cells.length ?? 0,
          geometry: {
            scrollLeft: wrapper.scrollWidth - wrapper.clientWidth,
            scrollWidth: wrapper.scrollWidth,
            clientWidth: wrapper.clientWidth,
            wrapperLeft: wrapperRect.left,
            wrapperRight: wrapperRect.right,
            lastCellLeft: lastCellRect?.left ?? null,
            lastCellRight: lastCellRect?.right ?? null,
          },
        };
      });

      const diagramGrids = Array.from(document.querySelectorAll('.diagram-grid')).map(
        (grid, index) => {
          const rect = grid.getBoundingClientRect();
          const cardOverflow = Array.from(grid.children).some((card) => {
            const cardRect = card.getBoundingClientRect();
            return cardRect.left < rect.left - tolerance || cardRect.right > rect.right + tolerance;
          });
          return {
            index,
            contained:
              rect.left >= -tolerance && rect.right <= viewportWidth + tolerance && !cardOverflow,
          };
        },
      );

      return {
        viewportWidth,
        documentWidth,
        tables,
        diagramGrids,
        expected,
      };
    },
    {
      tableWrapperSelector: TABLE_WRAPPER_SELECTOR,
      wideTableSelector: WIDE_TABLE_SELECTOR,
      expected: definition.expect,
    },
  );

  if (report.documentWidth > report.viewportWidth + 1) {
    failures.push(
      `document horizontal overflow (${report.documentWidth}px > ${report.viewportWidth}px)`,
    );
  }

  if (report.tables.length < definition.expect.tables) {
    failures.push(
      `expected at least ${definition.expect.tables} tables, found ${report.tables.length}`,
    );
  }

  for (const table of report.tables) {
    const label = `table ${table.index + 1}`;
    if (!table.wrapperFound) {
      failures.push(`${label} is not inside ${TABLE_WRAPPER_SELECTOR}`);
      continue;
    }
    if (!table.wrapperWithinViewport) {
      failures.push(`${label} wrapper extends outside the 320px viewport`);
    }
    if (table.columns > 1 && !table.finalColumnVisible) {
      const { geometry } = table;
      failures.push(
        `${label} final column's right edge is not reachable after scrolling its wrapper `
        + `(cell ${geometry.lastCellLeft}–${geometry.lastCellRight}px; `
        + `wrapper ${geometry.wrapperLeft}–${geometry.wrapperRight}px; `
        + `scroll ${geometry.scrollLeft}/${geometry.scrollWidth - geometry.clientWidth}px)`,
      );
    }
  }

  if (report.diagramGrids.length < definition.expect.diagramGrids) {
    failures.push(
      `expected at least ${definition.expect.diagramGrids} diagram grids, found ${report.diagramGrids.length}`,
    );
  }

  for (const grid of report.diagramGrids) {
    if (!grid.contained) {
      failures.push(`diagram grid ${grid.index + 1} or one of its cards escapes the viewport`);
    }
  }

  return failures;
}

async function main() {
  configureNixBrowserCompatibility();
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-gpu', '--disable-software-rasterizer'],
  });
  const context = await browser.newContext({ viewport: VIEWPORT });
  const page = await context.newPage();
  let failureCount = 0;

  try {
    for (const definition of PAGES) {
      const failures = await inspectPage(page, definition);
      if (failures.length === 0) {
        console.log(`PASS  ${definition.name} at ${VIEWPORT.width}px`);
        continue;
      }

      failureCount += failures.length;
      for (const failure of failures) {
        printFailure(definition.name, failure);
      }
    }
  } finally {
    await context.close();
    await browser.close();
  }

  if (failureCount > 0) {
    console.error(`\n${failureCount} phone-overflow check(s) failed.`);
    process.exit(1);
  }

  console.log(`\nAll ${PAGES.length} representative pages passed at ${VIEWPORT.width}px.`);
}

main().catch((error) => {
  console.error(`Phone overflow QA could not run: ${error.stack || error.message}`);
  process.exit(1);
});