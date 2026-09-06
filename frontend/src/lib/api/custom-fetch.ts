const getUrl = (contextUrl: string): string => {
  const baseUrl = process.env.DEPLOY_ENV === "PROD"
    ? "http://backend:8010"
    : "http://localhost:8010";

  const requestUrl = new URL(contextUrl, baseUrl);

  return requestUrl.toString();
};

export const customFetch = async <T>(
  url: string,
  options?: RequestInit,
): Promise<T> => {
  const baseUrl = getUrl(url);
  const response = await fetch(baseUrl, options);

  const body = [204, 205, 304].includes(response.status)
    ? null
    : await response.text();
  const data = body ? JSON.parse(body) : {};

  return { data, status: response.status, headers: response.headers } as T;
};
