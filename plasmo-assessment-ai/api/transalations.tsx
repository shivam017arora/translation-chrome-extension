import axiosInstance from "./axios";

//get a translation given word and target
export const getTranslation = async (word, target) => {
    return new Promise((resolve, reject) => {
        axiosInstance
          .get(`/translations?word=${word}&language=${target}`)
          .then((res) => {
            resolve(res.data)
          })
          .catch((err) => {
            reject(err)
          })
    }
    );
}

//get all translations 
export const getAllTranslations = async () => {
    return new Promise((resolve, reject) => {
        axiosInstance
          .get(`/translations`)
          .then((res) => {
            resolve(res.data)
          })
          .catch((err) => {
            reject(err)
          })
    }
    );
}