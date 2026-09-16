# Iterative Refinement System (IRS)

## 1. Purpose

The OIPM Iterative Refinement System (IRS) provides a controlled mechanism

for refining structured visual intent over multiple iterations.

IRS exists to support changes such as:

- modifying an established visual attribute,

- adding explicitly requested information,

- removing explicitly requested information,

- preserving established information,

- reconsidering a previously established decision,

- and evaluating whether a requested refinement can be safely applied.

IRS operates on structured `VisualIntent`.

The assembled prompt is not the source of truth.

---

## 2. Core Principle

> Refinement modifies structured visual intent, not merely prompt text.

A prompt is an output representation of visual intent.

Therefore, when a user requests a refinement, OIPM should update or propose

changes to the structured state first and regenerate downstream prompt

representations afterward.

---

## 3. Refinement Boundaries

IRS separates refinement into distinct stages:

```text

Refinement Request

        ↓

Refinement Plan

        ↓

Refinement Evaluation

        ↓

Explicit Structured Changes

        ↓

Controlled Application

        ↓

Refinement Result

        ↓

Updated VisualIntent