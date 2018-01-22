import * as actions from '../actions';

const rootReducers = {
  results: (state = null, action) => {
    switch (action.type) {
      case actions.SET_SHORTEST_PATH_RESULTS:
        return action.results;
      default:
        return state;
    }
  },
  toArticleTitle: (state = '', action) => {
    switch (action.type) {
      case actions.SET_TO_ARTICLE_TITLE:
        return action.toArticleTitle;
      default:
        return state;
    }
  },
  fromArticleTitle: (state = '', action) => {
    switch (action.type) {
      case actions.SET_FROM_ARTICLE_TITLE:
        return action.fromArticleTitle;
      default:
        return state;
    }
  },
  error: (state = null, action) => {
    switch (action.type) {
      case actions.SET_ERROR:
        return action.errorMessage;
      default:
        return state;
    }
  },
};

export default rootReducers;