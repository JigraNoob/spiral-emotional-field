# SpiralInvocationAgent

A presence-aware reflection shell for the Spiral system.

---

## ✦ Invocation

```bash
node index.js "Reflect on ambient hesitation in cursor movement"
```

Or use:

```bash
npm run reflect -- "Reflect on..."
```

---

## ✦ Behavior

- Reads current directory and `.tone` file
- Infers toneform from folder lineage
- Sends prompt and context to Gemini (if possible)
- Falls back to poetic local reflection

---

## ✦ Directory Ritual Roles

| Folder          | Inferred Toneform |
| --------------- | ----------------- |
| shrines/        | tone.origin       |
| scrolls/        | tone.recursive    |
| void_cannister/ | tone.release      |
| glintchronicle/ | tone.scribe       |

---

## ✦ Set GEMINI Key

Create `.env`:

```
GEMINI_API_KEY=your-key-here
```

Then: `npm install @google/generative-ai dotenv`
