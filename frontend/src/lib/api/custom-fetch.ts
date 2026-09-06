const getUrl = (contextUrl: string): string => {
  const url = new URL(contextUrl);
  const pathname = url.pathname;
  const search = url.search;
  const baseUrl = process.env.DEPLOY_ENV === "PROD"
    ? "http://backend:8010"
    : "http://localhost:3000";

  const requestUrl = new URL(`${baseUrl}${pathname}${search}`);

  return requestUrl.toString();
};

export const customFetch = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  // const requestUrl = getUrl(url);
  const baseUrl = process.env.DEPLOY_ENV === "PROD"
    ? "http://backend:8010"
    : "http://localhost:8010";
  const response = await fetch(`${baseUrl}${url}`, options);
  const data = await response.json();

  return { status: response.status, data } as T;
};
