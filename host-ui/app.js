const LONG_URL =
  "https://example.com/a/very/long/path/that/keeps/going/without/introducing/layout/overflow?query=host-ui-structural-validation&mode=local";

const makeLongMessages = () =>
  Array.from({ length: 42 }, (_, index) => {
    const outgoing = index % 3 === 1;
    const number = index + 1;
    let text = outgoing
      ? `Local outgoing message ${number}. This is a reading-position and scrolling fixture.`
      : `Incoming fixture ${number}. The Host owns message order, alignment, metadata, and overflow behavior.`;

    if (index === 8) {
      text = `Long URL fixture:\n${LONG_URL}`;
    }
    if (index === 18) {
      text =
        "Long unbroken content fixture:\nHOST_UI_" +
        "STRUCTURALVALIDATION".repeat(16);
    }
    if (index === 27) {
      text =
        "Multiline fixture:\nFirst line keeps its break.\nSecond line stays readable.\nThird line confirms bubble growth.";
    }

    return {
      id: `long-${number}`,
      role: outgoing ? "outgoing" : "incoming",
      text,
      time: `${9 + Math.floor(index / 12)}:${String((index * 7) % 60).padStart(2, "0")}`,
      status: outgoing ? "Delivered" : "",
    };
  });

const seedConversations = [
  {
    id: "welcome",
    title: "Host UI structure review",
    preview: "A neutral baseline for layout and behavior.",
    time: "Now",
    messages: [
      {
        id: "welcome-1",
        role: "incoming",
        text: "This local prototype validates the complete Host UI shell before visual theme work begins.",
        time: "10:01",
        status: "",
      },
      {
        id: "welcome-2",
        role: "outgoing",
        text: "Keep structure, accessibility, and interaction behavior owned by the Host.",
        time: "10:02",
        status: "Delivered",
      },
      {
        id: "welcome-3",
        role: "incoming",
        text: "All data on this screen is deterministic local mock data. No backend is connected.",
        time: "10:03",
        status: "",
      },
    ],
  },
  {
    id: "long",
    title:
      "An intentionally very long conversation title used to validate truncation in both the sidebar and the chat header",
    preview: "Long messages, URLs, multiline content, and scrolling.",
    time: "9:42",
    messages: makeLongMessages(),
  },
  {
    id: "empty-fixture",
    title: "Empty conversation fixture",
    preview: "No messages yet",
    time: "Tue",
    messages: [],
  },
  {
    id: "planning",
    title: "Application shell notes",
    preview: "Header and composer remain visible.",
    time: "Mon",
    messages: [
      {
        id: "planning-1",
        role: "incoming",
        text: "The sidebar list and the message viewport own independent scroll regions.",
        time: "14:12",
        status: "",
      },
    ],
  },
  ...Array.from({ length: 20 }, (_, index) => ({
    id: `archive-${index + 1}`,
    title:
      index === 7
        ? "Another extremely long archived title that must truncate without increasing the width of the sidebar"
        : `Local archived conversation ${String(index + 1).padStart(2, "0")}`,
    preview:
      index % 2
        ? "A short local preview for sidebar scrolling."
        : "Mock content remains local and is not persisted.",
    time: index < 5 ? "Sun" : "Jul",
    messages: [
      {
        id: `archive-${index + 1}-message`,
        role: index % 2 ? "outgoing" : "incoming",
        text: `Archived local fixture ${index + 1}.`,
        time: "11:30",
        status: index % 2 ? "Delivered" : "",
      },
    ],
  })),
];

const state = {
  conversations: structuredClone(seedConversations),
  activeId: "welcome",
  filter: "",
  demoState: "conversation",
  drawerOpen: false,
  drawerOpener: null,
  isComposing: false,
};

const app = document.querySelector("#app");
const titleElement = document.querySelector("#conversation-title");
const viewport = document.querySelector("#message-viewport");
const composer = document.querySelector("#composer");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const statusLiveRegion = document.querySelector("#host-status-live-region");
const demoState = document.querySelector("#demo-state");
const appearanceToggle = document.querySelector("#appearance-toggle");
const openDrawerButton = document.querySelector("#open-drawer");
const drawer = document.querySelector("#mobile-drawer");
const backdrop = document.querySelector("#drawer-backdrop");
const devHarness = document.querySelector("#dev-harness");
const queryParams = new URLSearchParams(window.location.search);
const devMode = queryParams.get("dev") === "1";
const decorationFixture = devMode ? queryParams.get("decorations") : null;
const allowedDecorationFixtures = new Set(["bubble-inside", "bubble-outside", "avatar-outside"]);

if (devMode) {
  devHarness.hidden = false;
}

if (allowedDecorationFixtures.has(decorationFixture)) {
  app.dataset.validationDecoration = decorationFixture;
}

const activeConversation = () =>
  state.conversations.find((conversation) => conversation.id === state.activeId);

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

function sidebarMarkup(isDrawer) {
  return `
    <div class="brand-area" data-component="brand-area" data-theme-hook="brand-area">
      <div class="decoration-boundary decoration-boundary--outside" aria-hidden="true">
        <div
          class="decoration-slot"
          aria-hidden="true"
          data-theme-hook="brand-decoration-outside"
        ></div>
      </div>
      <div class="decoration-boundary decoration-boundary--inside" aria-hidden="true">
        <div
          class="decoration-slot"
          aria-hidden="true"
          data-theme-hook="brand-decoration-inside"
        ></div>
      </div>
      <div class="brand-content content-layer">
        <div class="brand-mark" aria-hidden="true">AI</div>
        <div>
          <p class="brand-name">Host UI</p>
          <p class="brand-detail">Structural prototype</p>
        </div>
        ${
          isDrawer
            ? `<button class="icon-button drawer-close" type="button" aria-label="Close conversation sidebar">
                <span aria-hidden="true">×</span>
              </button>`
            : ""
        }
      </div>
    </div>
    <div class="sidebar-controls">
      <button
        class="new-chat-button"
        data-action="new-chat"
        data-component="new-chat-button"
        data-theme-hook="new-chat-button"
        type="button"
      >
        <span aria-hidden="true">＋</span>
        <span>New chat</span>
      </button>
      <label class="search-label">
        <span>Search conversations</span>
        <input
          class="search-input"
          data-role="conversation-search"
          data-component="conversation-search"
          data-theme-hook="conversation-search"
          type="search"
          value="${escapeHtml(state.filter)}"
          placeholder="Filter by title"
          autocomplete="off"
        />
      </label>
    </div>
    <ul
      class="conversation-list"
      data-role="conversation-list"
      data-component="conversation-list"
      aria-label="Conversations"
    ></ul>
    <div
      class="account-area"
      data-component="account-settings-area"
      data-theme-hook="account-settings-area"
    >
      <button
        class="settings-button"
        type="button"
        aria-label="Account and settings unavailable"
        title="Unavailable in the structural prototype"
        aria-disabled="true"
        disabled
      >
        <span aria-hidden="true">○</span>
        <span>Account and settings</span>
      </button>
    </div>
  `;
}

function renderSidebarShells() {
  document.querySelectorAll("[data-sidebar-content]").forEach((container) => {
    container.innerHTML = sidebarMarkup(container.closest("#mobile-drawer") !== null);
  });
  bindSidebarEvents();
  renderConversationLists();
}

function bindSidebarEvents() {
  document.querySelectorAll('[data-action="new-chat"]').forEach((button) => {
    button.addEventListener("click", createConversation);
  });

  document.querySelectorAll('[data-role="conversation-search"]').forEach((search) => {
    search.addEventListener("input", (event) => {
      state.filter = event.target.value;
      document
        .querySelectorAll('[data-role="conversation-search"]')
        .forEach((otherSearch) => {
          if (otherSearch !== event.target) otherSearch.value = state.filter;
        });
      renderConversationLists();
    });
  });

  document.querySelector(".drawer-close")?.addEventListener("click", () => closeDrawer());
}

function renderConversationLists() {
  const query = state.filter.trim().toLocaleLowerCase();
  const filtered = state.conversations.filter((conversation) =>
    conversation.title.toLocaleLowerCase().includes(query),
  );

  document.querySelectorAll('[data-role="conversation-list"]').forEach((list) => {
    if (!filtered.length) {
      list.innerHTML = `<li class="conversation-list-empty">No matching conversations</li>`;
      return;
    }

    list.innerHTML = filtered
      .map(
        (conversation) => `
          <li class="conversation-item">
            <button
              class="conversation-button"
              type="button"
              data-conversation-id="${escapeHtml(conversation.id)}"
              data-component="conversation-item"
              data-theme-hook="conversation-item"
              aria-current="${conversation.id === state.activeId}"
              title="${escapeHtml(conversation.title)}"
            >
              <span class="conversation-item-title">${escapeHtml(conversation.title)}</span>
              <span class="conversation-time">${escapeHtml(conversation.time)}</span>
              <span class="conversation-preview">${escapeHtml(conversation.preview)}</span>
            </button>
          </li>
        `,
      )
      .join("");

    list.querySelectorAll("[data-conversation-id]").forEach((button) => {
      button.addEventListener("click", () => {
        selectConversation(button.dataset.conversationId);
      });
    });
  });
}

function createConversation() {
  const id = `local-${Date.now()}`;
  state.conversations.unshift({
    id,
    title: "New local conversation",
    preview: "No messages yet",
    time: "Now",
    messages: [],
  });
  state.filter = "";
  state.activeId = id;
  state.demoState = "conversation";
  demoState.value = state.demoState;
  renderSidebarShells();
  renderWorkspace({ scrollMode: "bottom" });
  if (state.drawerOpen) closeDrawer({ restoreFocus: false });
  input.focus();
}

function selectConversation(id) {
  state.activeId = id;
  state.demoState = "conversation";
  demoState.value = state.demoState;
  renderConversationLists();
  renderWorkspace({ scrollMode: "bottom" });
  if (state.drawerOpen) closeDrawer();
}

function statePanelMarkup(type) {
  if (type === "loading") {
    return `
      <div class="state-panel loading-state" data-component="loading-state">
        <div class="state-marker" aria-hidden="true">…</div>
        <h2>Loading conversation</h2>
        <p>Local fixture: content is temporarily being prepared.</p>
        <div class="loading-lines" aria-hidden="true">
          <span class="loading-line"></span>
          <span class="loading-line"></span>
          <span class="loading-line"></span>
        </div>
      </div>
    `;
  }

  if (type === "error") {
    return `
      <div
        class="state-panel error-state"
        data-component="error-state"
        data-theme-hook="error-state"
        role="alert"
      >
        <div class="state-marker" aria-hidden="true">!</div>
        <h2>Conversation could not be shown</h2>
        <p>This recoverable local error fixture includes text, an icon, and a retry action.</p>
        <button class="retry-button" type="button" data-action="retry">Try again</button>
      </div>
    `;
  }

  return `
    <div
      class="state-panel empty-state decorated-component"
      data-component="empty-state"
      data-theme-hook="empty-state"
    >
      <div class="decoration-boundary decoration-boundary--outside" aria-hidden="true">
        <div
          class="decoration-slot"
          aria-hidden="true"
          data-theme-hook="empty-state-decoration-outside"
        ></div>
      </div>
      <div class="decoration-boundary decoration-boundary--inside" aria-hidden="true">
        <div
          class="decoration-slot"
          aria-hidden="true"
          data-theme-hook="empty-state-decoration-inside"
        ></div>
      </div>
      <div class="content-layer content-layer--state">
        <div
          class="empty-state-slot"
          data-theme-hook="empty-state-illustration"
          aria-hidden="true"
        ></div>
        <h2>Start a local conversation</h2>
        <p>Messages sent here stay in memory for this page session and are not persisted.</p>
      </div>
    </div>
  `;
}

function messageMarkup(message) {
  const incoming = message.role === "incoming";
  const direction = incoming ? "incoming" : "outgoing";
  return `
    <article
      class="message-group message-group--${direction}"
      data-component="message-group"
      data-message-id="${escapeHtml(message.id)}"
    >
      <div
        class="avatar-frame"
        data-component="avatar-frame"
        data-theme-hook="avatar-frame"
        aria-label="${incoming ? "Host" : "You"}"
      >
        <div class="decoration-boundary decoration-boundary--outside" aria-hidden="true">
          <div
            class="decoration-slot"
            aria-hidden="true"
            data-theme-hook="avatar-frame-decoration-outside"
          ></div>
        </div>
        <div class="decoration-boundary decoration-boundary--inside" aria-hidden="true">
          <div
            class="decoration-slot"
            aria-hidden="true"
            data-theme-hook="avatar-frame-decoration-inside"
          ></div>
        </div>
        <span class="content-layer content-layer--avatar" aria-hidden="true">${incoming ? "AI" : "You"}</span>
      </div>
      <div class="message-body">
        <div
          class="bubble"
          data-component="${direction}-message"
          data-theme-hook="${direction}-bubble"
        >
          <div class="decoration-boundary decoration-boundary--outside" aria-hidden="true">
            <div
              class="decoration-slot"
              aria-hidden="true"
              data-theme-hook="${direction}-bubble-decoration-outside"
            ></div>
          </div>
          <div class="decoration-boundary decoration-boundary--inside" aria-hidden="true">
            <div
              class="decoration-slot"
              aria-hidden="true"
              data-theme-hook="${direction}-bubble-decoration-inside"
            ></div>
          </div>
          <div class="content-layer content-layer--bubble">
            <p>${escapeHtml(message.text)}</p>
          </div>
        </div>
        <footer class="message-meta">
          <time>${escapeHtml(message.time)}</time>
          ${
            message.status
              ? `<span class="delivery-state">${escapeHtml(message.status)}</span>`
              : ""
          }
        </footer>
      </div>
    </article>
  `;
}

function renderMessages(messages, scrollMode) {
  const previousScrollTop = viewport.scrollTop;
  const previousScrollHeight = viewport.scrollHeight;

  if (!messages.length) {
    viewport.innerHTML = statePanelMarkup("empty");
  } else {
    viewport.innerHTML = `
      <div class="message-list">
        ${messages.map(messageMarkup).join("")}
      </div>
    `;
  }

  requestAnimationFrame(() => {
    if (scrollMode === "bottom") {
      viewport.scrollTop = viewport.scrollHeight;
    } else if (scrollMode === "preserve") {
      viewport.scrollTop = Math.min(
        previousScrollTop,
        Math.max(0, viewport.scrollHeight - viewport.clientHeight),
      );
    } else if (scrollMode === "anchor-bottom") {
      viewport.scrollTop = previousScrollTop + (viewport.scrollHeight - previousScrollHeight);
    }
  });
}

function renderWorkspace({ scrollMode = "preserve" } = {}) {
  const conversation = activeConversation();
  titleElement.textContent = conversation?.title ?? "Conversation";
  titleElement.title = conversation?.title ?? "";
  const forcedState = state.demoState;
  const disabled = forcedState === "disabled" || forcedState === "loading";

  input.disabled = disabled;
  sendButton.disabled = disabled;
  input.placeholder =
    forcedState === "disabled"
      ? "Composer disabled for this fixture"
      : forcedState === "loading"
        ? "Loading conversation"
        : "Write a message";

  if (forcedState === "loading" || forcedState === "error") {
    viewport.innerHTML = statePanelMarkup(forcedState);
    announceStatus(
      forcedState === "loading"
        ? "Conversation loading."
        : "Conversation failed to load.",
    );
    viewport.querySelector('[data-action="retry"]')?.addEventListener("click", () => {
      state.demoState = "conversation";
      demoState.value = state.demoState;
      renderWorkspace({ scrollMode: "bottom" });
      input.focus();
    });
    return;
  }

  if (forcedState === "empty") {
    viewport.innerHTML = statePanelMarkup("empty");
    return;
  }

  renderMessages(conversation?.messages ?? [], scrollMode);
}

function resizeComposer() {
  input.style.height = "auto";
  const maxHeight = Number.parseFloat(
    getComputedStyle(document.documentElement).getPropertyValue("--composer-max-height"),
  );
  input.style.height = `${Math.min(input.scrollHeight, maxHeight)}px`;
  input.style.overflowY = input.scrollHeight > maxHeight ? "auto" : "hidden";
}

function isNearBottom() {
  return viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight <= 120;
}

function announceStatus(message) {
  statusLiveRegion.textContent = "";
  requestAnimationFrame(() => {
    statusLiveRegion.textContent = message;
  });
}

function sendMessage() {
  const text = input.value.trim();
  if (!text || input.disabled) return;

  const conversation = activeConversation();
  if (!conversation) return;

  const shouldFollowBottom = isNearBottom();
  const now = new Date();
  conversation.messages.push({
    id: `message-${Date.now()}`,
    role: "outgoing",
    text,
    time: now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    status: "Sent locally",
  });
  conversation.preview = text.replace(/\s+/g, " ");
  conversation.time = "Now";
  if (conversation.title === "New local conversation") {
    conversation.title = text.length > 48 ? `${text.slice(0, 48)}…` : text;
  }

  input.value = "";
  resizeComposer();
  renderConversationLists();
  renderWorkspace({ scrollMode: shouldFollowBottom ? "bottom" : "preserve" });
  announceStatus("Message sent.");
  input.focus();
}

function openDrawer() {
  if (matchMedia("(min-width: 48.0625rem)").matches) return;
  state.drawerOpen = true;
  state.drawerOpener = document.activeElement;
  app.dataset.drawerOpen = "true";
  openDrawerButton.setAttribute("aria-expanded", "true");
  drawer.setAttribute("aria-hidden", "false");
  document.querySelector(".main-workspace").setAttribute("inert", "");
  requestAnimationFrame(() => document.querySelector(".drawer-close")?.focus());
}

function closeDrawer({ restoreFocus = true } = {}) {
  if (!state.drawerOpen) return;
  state.drawerOpen = false;
  delete app.dataset.drawerOpen;
  openDrawerButton.setAttribute("aria-expanded", "false");
  drawer.setAttribute("aria-hidden", "true");
  document.querySelector(".main-workspace").removeAttribute("inert");
  if (restoreFocus) {
    const target = state.drawerOpener?.isConnected ? state.drawerOpener : openDrawerButton;
    target.focus();
  }
}

function trapDrawerFocus(event) {
  if (!state.drawerOpen || event.key !== "Tab") return;
  const focusable = [
    ...drawer.querySelectorAll(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [href], [tabindex]:not([tabindex="-1"])',
    ),
  ].filter((element) => !element.hidden && element.offsetParent !== null);

  if (!focusable.length) {
    event.preventDefault();
    drawer.focus();
    return;
  }

  const first = focusable[0];
  const last = focusable.at(-1);
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

composer.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage();
});

input.addEventListener("input", resizeComposer);
input.addEventListener("compositionstart", () => {
  state.isComposing = true;
});
input.addEventListener("compositionend", () => {
  state.isComposing = false;
});
input.addEventListener("keydown", (event) => {
  if (
    event.key === "Enter" &&
    !event.shiftKey &&
    !state.isComposing &&
    !event.isComposing
  ) {
    event.preventDefault();
    sendMessage();
  }
});

demoState.addEventListener("change", (event) => {
  state.demoState = event.target.value;
  renderWorkspace({ scrollMode: "bottom" });
});

appearanceToggle.addEventListener("click", () => {
  const dark = app.dataset.appearance !== "dark";
  app.dataset.appearance = dark ? "dark" : "light";
  appearanceToggle.setAttribute(
    "aria-label",
    dark
      ? "Use light neutral QA appearance"
      : "Use dark neutral QA appearance",
  );
});

openDrawerButton.addEventListener("click", openDrawer);
backdrop.addEventListener("click", () => closeDrawer());
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.drawerOpen) {
    event.preventDefault();
    closeDrawer();
    return;
  }
  trapDrawerFocus(event);
});

window.addEventListener("resize", () => {
  if (state.drawerOpen && matchMedia("(min-width: 48.0625rem)").matches) {
    closeDrawer({ restoreFocus: false });
  }
});

renderSidebarShells();
renderWorkspace({ scrollMode: "bottom" });
resizeComposer();
