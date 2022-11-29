export const cleanSearchParam = (text) =>
  text
    ?.normalize("NFD")
    ?.replace(/\p{Diacritic}/gu, "")
    ?.toUpperCase();
