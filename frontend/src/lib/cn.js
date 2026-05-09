/** Tiny className joiner — avoids pulling in clsx for one helper. */
export function cn(...args) {
  return args.filter(Boolean).join(" ");
}
